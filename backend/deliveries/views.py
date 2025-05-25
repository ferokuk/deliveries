from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.functions import TruncDay, TruncDate
from django.db.models import Count
from deliveries.models import Delivery, PackagingType, Service, CargoType
from deliveries.serializers import DeliverySerializer, PackagingTypeSerializer, ServiceSerializer, CargoTypeSerializer

from deliveries.pagination import DeliveriesPageNumberPagination

class DeliveryFilter(FilterSet):
    departure_datetime__gte = DateTimeFilter(field_name='departure_datetime', lookup_expr='date__gte')
    departure_datetime__lte = DateTimeFilter(field_name='departure_datetime', lookup_expr='date__lte')

    class Meta:
        model = Delivery
        fields = ['departure_datetime__gte', 'departure_datetime__lte', 'cargo_type', 'services']

class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = DeliverySerializer
    pagination_class = DeliveriesPageNumberPagination
    filterset_class = DeliveryFilter
    filter_backends = [
        DjangoFilterBackend,  # для фильтрации по полям filterset_fields
        filters.SearchFilter,  # для search_fields
        filters.OrderingFilter,  # для ordering_fields
    ]
    search_fields = [
        'transport_model__plate_number',
        'user__username',
    ]
    ordering_fields = ['departure_datetime', 'distance_km']
    ordering = ['-departure_datetime']

    def get_queryset(self):
        return Delivery.objects.select_related(
            'transport_model', 'packaging', 'cargo_type', 'user'
        ).prefetch_related('services').filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary_by_day(self, request):
        qs = self.get_queryset()
        params = request.query_params

        if params.get('departure_datetime__gte'):
            qs = qs.filter(departure_datetime__date__gte=params['departure_datetime__gte'])
        if params.get('departure_datetime__lte'):
            qs = qs.filter(departure_datetime__date__lte=params['departure_datetime__lte'])
        if params.get('cargo_type'):
            qs = qs.filter(cargo_type_id=params['cargo_type'])
        if params.get('services'):
            qs = qs.filter(services__id=params['services'])

        daily = (
            qs
            .annotate(day=TruncDay('departure_datetime'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        result = [
            {'day': item['day'], 'count': item['count']}
            for item in daily
        ]
        return Response(result)


class PackagingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
