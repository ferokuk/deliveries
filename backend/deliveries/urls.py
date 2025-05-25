from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from deliveries.views import DeliveryViewSet, CargoTypeViewSet, ServiceViewSet, PackagingTypeViewSet

router = DefaultRouter()
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'cargo', CargoTypeViewSet, basename='cargo')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'packaging', PackagingTypeViewSet, basename='packaging')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
