from django.contrib import admin
from models import SensorType, SensorData


def clear_sensor_data(model_admin, request, queryset):
    for sensor_type in queryset:
        SensorData.objects.filter(type=sensor_type).delete()
clear_sensor_data.short_description = "Clear sensor data"


class SensorTypeAdmin(admin.ModelAdmin):
    actions = [clear_sensor_data]

admin.site.register(SensorType, SensorTypeAdmin)
admin.site.register(SensorData)
