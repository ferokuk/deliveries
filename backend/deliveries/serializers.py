from rest_framework import serializers

from deliveries.models import Delivery, TransportModel, PackagingType, Service, CargoType, DeliveryStatusEnum


class TransportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportModel
        fields = ['id', 'plate_number']


class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingType
        fields = ['id', 'title']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ['id', 'name']


class DeliverySerializer(serializers.ModelSerializer):
    transport_model = TransportModelSerializer(read_only=True)
    packaging = PackagingTypeSerializer(read_only=True)
    services = ServiceSerializer(read_only=True, many=True)
    cargo_type = CargoTypeSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    user = serializers.StringRelatedField()

    class Meta:
        model = Delivery
        fields = '__all__'
