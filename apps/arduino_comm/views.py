from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

# Initial sensor configuration with 10 generic sensors
device_status = {
    f"sensor_{i+1}": {"id": f"sensor_{i+1}", "name": f"Sensor {i+1}", "type": "input", "status": "off", "value": 0}
    for i in range(10)
}

@csrf_exempt
def receive_data(request):
    """Endpoint to receive sensor data from Arduino"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                if key in device_status:
                    device_status[key]['value'] = value
            return JsonResponse({"message": "Data received", "status": device_status}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def send_command(request):
    """Endpoint to send control commands to Arduino"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            command = data.get("command")
            if sensor_id in device_status:
                device_status[sensor_id]['status'] = command
                return JsonResponse({"message": "Command sent", "status": device_status}, status=200)
            return JsonResponse({"error": "Unknown sensor"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def configure_sensor(request):
    """Endpoint to configure sensor name, type (input/output)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            name = data.get("name")
            sensor_type = data.get("type")
            if sensor_id in device_status:
                if name:
                    device_status[sensor_id]['name'] = name
                if sensor_type in ["input", "output"]:
                    device_status[sensor_id]['type'] = sensor_type
                return JsonResponse({"message": "Configuration updated", "status": device_status}, status=200)
            return JsonResponse({"error": "Unknown sensor"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

def control_page(request):
    """Render the control page where users can interact with Arduino"""
    return render(request, 'arduino_comm/control_panel.html', {"device_status": device_status})


def fetch_sensor_data(request):
    """Endpoint to fetch the current status of all sensors."""
    return JsonResponse(device_status, status=200)

    