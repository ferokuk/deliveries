from django.urls import path, include
from rest_framework.routers import DefaultRouter

from deliveries.views import DeliveryViewSet, CargoTypeViewSet, ServiceViewSet, PackagingTypeViewSet, \
    CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView

router = DefaultRouter()
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'cargo', CargoTypeViewSet, basename='cargo')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'packaging', PackagingTypeViewSet, basename='packaging')

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
