import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from models import SensorType, SensorData
from django.views.decorators.csrf import csrf_exempt
import datetime


def home(request):
    return render(request, 'index.html', {
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


def history(request, code, year, month, day):
    if request.method == 'GET':
        try:
            sensor = SensorType.objects.get(code=code)
            start_time = datetime.datetime(int(year), int(month), int(day))
            end_time = start_time + datetime.timedelta(days=1)

            # Get data for the given sensor code
            all_sensor_data = sensor.data.filter(time__range=(start_time, end_time)).all()
            sensor_data = []
            if all_sensor_data:
                for i in range(0, len(all_sensor_data) - 1):
                    if all_sensor_data[i].time.minute != all_sensor_data[i + 1].time.minute:
                        sensor_data += [all_sensor_data[i]]
            return render(request, 'history.html', {
                'date': start_time,
                'previous_date': start_time - datetime.timedelta(days=1),
                'next_date': end_time,
                'sensor': sensor,
                'sensor_data': reversed(sensor_data),
            })
        except SensorType.DoesNotExist:
            return HttpResponseForbidden

    return HttpResponseForbidden
