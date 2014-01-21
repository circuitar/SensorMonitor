import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from models import SensorType, SensorData
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'index.htm', {
        'sensors': SensorType.objects.all(),
    })


@csrf_exempt
def sensor(request):
    if request.method == 'GET':
        response_data = {}

        # Get the latest sensor data for each sensor type
        for sensor in SensorType.objects.all():
            sensor_data = sensor.data.first()
            if sensor_data:
                response_data[sensor.code] = sensor_data.value

        # Send the result as JSON
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if request.method == 'POST':
        # Check if the sensor code exists and store the value in the database
        for sensor, value in request.POST.items():
            try:
                sensor_type = SensorType.objects.get(code=sensor)
                sensor_data = SensorData()
                sensor_data.type = sensor_type
                sensor_data.value = float(value)
                sensor_data.save()
            except (SensorType.DoesNotExist, ValueError):
                pass

        return HttpResponse()

    return HttpResponseForbidden
