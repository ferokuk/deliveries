from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from deliveries.models import (
    TransportModel, PackagingType, Service, CargoType, Delivery, DeliveryStatusEnum
)
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class DeliveryAPITestCase(APITestCase):
    def setUp(self):
        # Создаём пользователя и токен
        self.user = User.objects.create_user(username='testuser', password='pass')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Справочники
        self.transport = TransportModel.objects.create(plate_number='А123ВС')
        self.packaging = PackagingType.objects.create(title='Box')
        self.service1 = Service.objects.create(name='Express')
        self.service2 = Service.objects.create(name='Fragile')
        self.cargo = CargoType.objects.create(name='Electronics')

        # Файл для загрузки
        self.pdf_file = SimpleUploadedFile(
            "test.pdf", b"%PDF-1.4 test", content_type="application/pdf"
        )

        # Создаём одну доставку
        now = datetime.now()
        self.delivery = Delivery.objects.create(
            transport_model=self.transport,
            departure_datetime=now,
            arrival_datetime=now + timedelta(hours=2),
            distance_km='123.45',
            media_file=self.pdf_file,
            status=DeliveryStatusEnum.PENDING.value,
            packaging=self.packaging,
            cargo_type=self.cargo,
            technical_state='ok',
            user=self.user
        )
        self.delivery.services.set([self.service1, self.service2])

    def test_list_deliveries(self):
        """GET /deliveries/ возвращает список доставок пользователя."""
        url = reverse('delivery-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['id'], self.delivery.id)

    def test_retrieve_delivery(self):
        """GET /deliveries/{id}/ возвращает детальную информацию."""
        url = reverse('delivery-detail', args=[self.delivery.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data
        service_ids = [s['id'] for s in data['services']]
        self.assertEqual(data['transport_model']['id'], self.transport.id)
        self.assertEqual(data['status'], DeliveryStatusEnum.PENDING.value)
        self.assertIn(self.service1.id, service_ids)
        self.assertIn(self.service2.id, service_ids)

    def test_filter_by_status(self):
        """Фильтрация по статусу доставки."""
        url = reverse('delivery-list') + '?status=pending'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

        # Нет доставок со статусом 'delivered'
        url = reverse('delivery-list') + '?status=delivered'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_ordering_distance(self):
        """Сортировка по дистанции."""
        # Добавим ещё одну доставку с другим distance_km
        now = datetime.now()
        d2 = Delivery.objects.create(
            transport_model=self.transport,
            departure_datetime=now - timedelta(days=1),
            arrival_datetime=now,
            distance_km='50.00',
            media_file=self.pdf_file,
            packaging=self.packaging,
            technical_state='ok',
            user=self.user
        )
        d2.services.set([self.service1])
        url = reverse('delivery-list') + '?ordering=distance_km'
        resp = self.client.get(url)
        distances = [item['distance_km'] for item in resp.data]
        # Проверяем, что он сортирует по возрастанию
        self.assertEqual(distances, ['50.00', '123.45'])

    def test_search_by_plate(self):
        """Поиск по номеру транспорта."""
        url = reverse('delivery-list') + '?search=А123'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_date_filters(self):
        """Фильтрация по диапазону дат отправления."""
        url = reverse('delivery-list') + (
            f'?departure_datetime__gte={self.delivery.departure_datetime.isoformat()}'
        )
        print(f'{self.delivery.departure_datetime.isoformat()=}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

        # Дата позже, чем у существующей доставки
        future = (self.delivery.departure_datetime + timedelta(days=1)).isoformat()
        url = reverse('delivery-list') + f'?departure_datetime__gte={future}'
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 0)
