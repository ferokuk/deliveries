from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

from deliveries_test_task import settings

# Допустимые буквы для государственных номерных знаков
PLATE_LETTERS = 'АВЕКМНОРСТУХ'
PLATE_REGEX = RegexValidator(
    regex=rf'^[{PLATE_LETTERS}]\d{{3}}[{PLATE_LETTERS}]{{2}}$',
    message=(
        'Номер должен быть в формате 1 буква, 3 цифры, 2 буквы '
        '(буквы из набора А,В,Е,К,М,Н,О,Р,С,Т,У,Х).'
    ),
    code='invalid_plate'
)


class TransportModel(models.Model):
    plate_number = models.CharField(
        verbose_name="Номер транспорта",
        max_length=6,
        validators=[PLATE_REGEX],
        unique=True
    )

    def __str__(self):
        return self.plate_number

    class Meta:
        verbose_name = "Номер транспорта"
        verbose_name_plural = "Номера транспорта"


class PackagingType(models.Model):
    title = models.CharField(
        verbose_name="Тип упаковки",
        max_length=100
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип упаковки"
        verbose_name_plural = "Типы упаковки"


class Service(models.Model):
    name = models.CharField(
        verbose_name="Услуга",
        max_length=100
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class DeliveryStatusEnum(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    IN_TRANSIT = 'in_transit', 'В пути'
    DELIVERED = 'delivered', 'Доставлено'
    CANCELLED = 'cancelled', 'Отменено'


class CargoType(models.Model):
    name = models.CharField(
        verbose_name="Тип груза",
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип груза"
        verbose_name_plural = "Типы груза"


class Delivery(models.Model):
    # 1. Транспорт
    transport_model = models.ForeignKey(
        TransportModel,
        on_delete=models.PROTECT,
        verbose_name="Модель транспорта"
    )

    # 2. Время отправки и доставки
    departure_datetime = models.DateTimeField(
        verbose_name="Время отправления"
    )
    arrival_datetime = models.DateTimeField(
        verbose_name="Время доставки"
    )

    # 3. Вычисляемая длительность (не хранится в БД)
    @property
    def duration(self):
        """Возвращает timedelta между отправлением и доставкой."""
        return self.arrival_datetime - self.departure_datetime

    # 4. Дистанция (в километрах)
    distance_km = models.DecimalField(
        verbose_name="Дистанция, км",
        max_digits=7,
        decimal_places=2
    )

    # 5. Медиафайл — загрузка одного PDF или изображения
    media_file = models.FileField(
        verbose_name="Медиафайл",
        upload_to='deliveries/media/',
        help_text="PDF или изображение",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'],
                message='Допустимые форматы: PDF, JPG, JPEG, PNG.'
            )
        ]
    )

    # 6. Услуга — несколько опций
    services = models.ManyToManyField(
        Service,
        verbose_name="Услуги",
        related_name='deliveries'
    )

    # 7. Статус доставки
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatusEnum.choices,
        default=DeliveryStatusEnum.PENDING,
        verbose_name="Статус доставки"
    )

    # 8. Упаковка — одна опция
    packaging = models.ForeignKey(
        PackagingType,
        on_delete=models.PROTECT,
        verbose_name="Упаковка"
    )

    # 9. Тип груза (опционально)
    cargo_type = models.ForeignKey(
        CargoType,
        on_delete=models.PROTECT,
        verbose_name="Тип груза",
        blank=True,
        null=True
    )

    # 10. Техническое состояние — всего два варианта
    TECH_STATE_CHOICES = [
        ('ok', 'Исправно'),
        ('nok', 'Неисправно'),
    ]
    technical_state = models.CharField(
        verbose_name="Техническое состояние",
        max_length=3,
        choices=TECH_STATE_CHOICES,
        default='ok'
    )

    # 11. Пользователь
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='deliveries',
        verbose_name="Пользователь"
    )

    def __str__(self):
        return f"Доставка #{self.id} ({self.transport_model})"

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"
        ordering = ['-departure_datetime']
