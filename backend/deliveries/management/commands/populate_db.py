import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from deliveries.models import TransportModel, PackagingType, Service, CargoType
from deliveries.models import Delivery, DeliveryStatusEnum

User = get_user_model()

# Дополнительные справочники для заполнения
DEFAULT_PACKAGINGS = [
    'Пакет до 1 кг',
    'Целофан',
    'Коробка',
]
DEFAULT_SERVICES = [
    'До клиента',
    'Экспресс',
    'Страховка',
]
DEFAULT_CARGO_TYPES = [
    'Общий груз',
    'Опасный груз',
    'Рефрижераторный груз',
    'Хрупкий груз',
    'Мед.товары'
]

# Для генерации случайного номера по ГОСТ
PLATE_LETTERS = 'АВЕКМНОРСТУХ'


class Command(BaseCommand):
    help = 'Заполнить базу данных справочниками и случайными Delivery согласно модели.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=100,
            help='Количество доставок для создания.'
        )

    def handle(self, *args, **options):
        count = options['count']

        # Создаём или получаем записи справочников
        for _ in range(1000):
            plate = (
                    random.choice(PLATE_LETTERS)
                    + ''.join(random.choice('0123456789') for _ in range(3))
                    + ''.join(random.choice(PLATE_LETTERS) for _ in range(2))
            )
            TransportModel.objects.get_or_create(plate_number=plate)
        for title in DEFAULT_PACKAGINGS:
            PackagingType.objects.get_or_create(title=title)
        for svc in DEFAULT_SERVICES:
            Service.objects.get_or_create(name=svc)
        for ctype in DEFAULT_CARGO_TYPES:
            CargoType.objects.get_or_create(name=ctype)

        transports = list(TransportModel.objects.all())
        services = list(Service.objects.all())
        packages = list(PackagingType.objects.all())
        cargo_types = list(CargoType.objects.all()) or [None]
        users = list(User.objects.filter(is_active=True))
        statuses = [choice[0] for choice in DeliveryStatusEnum.choices]

        if not (transports and services and packages and users):
            self.stderr.write(self.style.ERROR(
                'Убедитесь, что справочники и хотя бы один активный пользователь существуют.'
            ))
            return

        for _ in range(count):
            transport_model = random.choice(transports)
            departure = timezone.now() - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
            arrival = departure + timedelta(hours=random.randint(1, 48), minutes=random.randint(0, 59))

            delivery = Delivery.objects.create(
                transport_model=transport_model,
                departure_datetime=departure,
                arrival_datetime=arrival,
                distance_km=round(random.uniform(1.0, 3000.0), 2),
                media_file=None,
                status=random.choice(statuses),
                packaging=random.choice(packages),
                cargo_type=random.choice(cargo_types),
                technical_state=random.choice(['ok', 'nok']),
                user=random.choice(users)
            )
            chosen_services = random.sample(services, k=random.randint(1, min(3, len(services))))
            delivery.services.set(chosen_services)

            self.stdout.write(f'\rСоздана доставка #{delivery.id}')

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {count} доставок.'))
