from django.contrib import admin

from deliveries.models import TransportModel, PackagingType, Service, CargoType, Delivery


@admin.register(TransportModel)
class TransportModelAdmin(admin.ModelAdmin):
    list_display = ('plate_number',)
    search_fields = ('plate_number',)


@admin.register(PackagingType)
class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'departure_datetime',
        'arrival_datetime',
        'duration_display',
        'transport_model',
        'distance_km',
        'status',
        'get_services',
        'packaging',
        'cargo_type',
        'technical_state',
        'user',
    )
    list_filter = (
        'departure_datetime',
        'arrival_datetime',
        'status',
        'services',
        'packaging',
        'cargo_type',
        'technical_state',
        'user',
    )
    search_fields = (
        'transport_model__plate_number',
        'services__name',
        'user__username',
    )
    ordering = ('-departure_datetime',)
    filter_horizontal = ('services',)  # удобная множественная фильтрация

    # Показать длительность в человекочитаемом виде
    def duration_display(self, obj):
        delta = obj.duration
        # формат «X ч Y м»
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes = remainder // 60
        return f"{int(hours)} ч {int(minutes)} м"

    duration_display.short_description = "Время в пути"

    # Список услуг через запятую
    def get_services(self, obj):
        return ", ".join(s.name for s in obj.services.all())

    get_services.short_description = "Услуги"

    def transport_model(self, obj):
        return obj.transport_model.plate_number

    transport_model.short_description = "Модель транспорта"
