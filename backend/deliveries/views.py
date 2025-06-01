from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncDay
from django.db.models import Count

from deliveries.auth import CookieJWTAuthentication
from deliveries.models import Delivery, PackagingType, Service, CargoType
from deliveries.serializers import DeliverySerializer, PackagingTypeSerializer, ServiceSerializer, CargoTypeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from deliveries.pagination import DeliveriesPageNumberPagination
from rest_framework.views import APIView
from rest_framework import status

from deliveries_test_task import settings


class DeliveryFilter(FilterSet):
    departure_datetime__gte = DateTimeFilter(field_name='departure_datetime', lookup_expr='date__gte')
    departure_datetime__lte = DateTimeFilter(field_name='departure_datetime', lookup_expr='date__lte')

    class Meta:
        model = Delivery
        fields = ['departure_datetime__gte', 'departure_datetime__lte', 'cargo_type', 'services']


class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
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
    authentication_classes = [CookieJWTAuthentication]
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    ordering = ['id']


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    ordering = ['id']


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    ordering = ['id']


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            data = response.data
            access = data.get("access")
            refresh = data.get("refresh")
            res = Response({'status': 'success', "detail": "Login successful"}, status=200)
            res.set_cookie(
                'access_token',
                access,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            )
            res.set_cookie(
                'refresh_token',
                refresh,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
            )
            # можно и refresh сохранить в куку, если хочешь
            return res

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh_token')
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data['access']
            res = Response({'detail': 'Token refreshed'}, status=status.HTTP_200_OK)
            res.set_cookie(
                'access_token',
                access,
                httponly=True,
                secure=True,
                samesite='None',
            )
            return res
        return response


class LogoutView(APIView):
    def post(self, request):
        res = Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)
        res.delete_cookie('access_token', samesite='None')
        res.delete_cookie('refresh_token', samesite='None')
        return res
