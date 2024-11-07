

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sensor
import json

# Initialize sensors
def initialize_sensors():
    for i in range(10):
        sensor_id = f"sensor_{i+1}"
        if not Sensor.objects.filter(id=sensor_id).exists():
            Sensor.objects.create(
                id=sensor_id,
                name=f"Sensor {i+1}",
                type="input",
                mode="digital",
                status="off",
                value=0,
                active=False
            )
            sensor.save()
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            for key, value in data.items():
                sensor = Sensor.objects.get(id=key)
                if isinstance(value, int):
                    sensor.value = value
                    sensor.status = 'high' if value else 'low'
                elif value in ['high', 'low']:
                    sensor.status = value
                    sensor.value = 1 if value == 'high' else 0
                else:
                    sensor.value = value  # Assuming it's already an integer
                sensor.save()
            return JsonResponse({"message": "Data received"}, status=200)
        except (json.JSONDecodeError, Sensor.DoesNotExist):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def send_command(request):
    """Update status or values for commands like high, low, or analog settings."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            command = data.get("command")
            value = data.get("value")

            sensor = Sensor.objects.get(id=sensor_id)
            if command in ["high", "low"] and sensor.mode == "digital":
                sensor.status = command  # Set high or low
            elif command == "set_value" and sensor.mode == "analog":
                sensor.value = value  # Set analog value
            sensor.save()

            return JsonResponse({"message": "Command sent successfully"}, status=200)
        except (json.JSONDecodeError, Sensor.DoesNotExist):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def configure_sensor(request):
    """Update sensor attributes like name, type, mode, and active state"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            sensor = get_object_or_404(Sensor, id=sensor_id)

            if "name" in data:
                sensor.name = data["name"]
            if "type" in data:
                sensor.type = data["type"]
            if "mode" in data:
                sensor.mode = data["mode"]
            if "active" in data:
                sensor.active = data["active"]

            sensor.save()
            return JsonResponse({"message": "Configuration updated successfully"}, status=200)
        except (json.JSONDecodeError, Sensor.DoesNotExist) as e:
            return JsonResponse({"error": "Invalid JSON or Sensor not found", "details": str(e)}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

def control_page(request):
    """Render the control page for interacting with Arduino"""
    initialize_sensors()
    device_status = Sensor.objects.all()
    return render(request, 'arduino_comm/control_panel.html', {"device_status": device_status})

@csrf_exempt
def save_sensors(request):
    """Save sensor data for all fields including type, mode, value, and status in one request."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for sensor_data in data.get("sensors", []):
                sensor_id = sensor_data.get("sensor_id")
                sensor = Sensor.objects.get(id=sensor_id)

                # Update all fields based on data received
                sensor.name = sensor_data.get("name", sensor.name)
                sensor.type = sensor_data.get("type", sensor.type)
                sensor.mode = sensor_data.get("mode", sensor.mode)
                sensor.active = sensor_data.get("active", sensor.active)
                sensor.value = sensor_data.get("value", sensor.value)
                sensor.status = sensor_data.get("status", sensor.status)  # For digital high/low

                sensor.save()

            return JsonResponse({"message": "All sensors updated successfully"}, status=200)
        except (json.JSONDecodeError, Sensor.DoesNotExist) as e:
            return JsonResponse({"error": "Invalid JSON or Sensor not found", "details": str(e)}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)


def fetch_sensor_data(request):
    """Endpoint to fetch the current status of all sensors."""
    sensors = Sensor.objects.all()
    data = {sensor.id: {
                "name": sensor.name,
                "type": sensor.type,
                "mode": sensor.mode,
                "status": sensor.status,
                "value": sensor.value,
                "active": sensor.active
            } for sensor in sensors}
    return JsonResponse(data)

def active_sensors_page(request):
    """Render a page displaying only active sensors."""
    initialize_sensors()  # Ensure sensors are initialized
    sensors = Sensor.objects.all()  # Fetch all sensors
    active_sensors = [sensor for sensor in sensors if sensor.active]  # Filter for active sensors
    return render(request, 'arduino_comm/active_sensors.html', {"device_status": active_sensors})


