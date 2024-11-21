from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required
import json
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["pai"]

# Helper function: Check superuser
def superuser_required(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True

# Initialize sensors in MongoDB
def initialize_sensors():
    """Ensure default sensors exist in the MongoDB collection."""
    # List of default sensors
    default_sensors = [
        {
            "id": "sensor_1",
            "name": "USA BIROU",
            "type": "output",
            "mode": "digital",
            "status": "low",
            "value": 76,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_2",
            "name": "USA INTRARE",
            "type": "output",
            "mode": "digital",
            "status": "low",
            "value": 243,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_3",
            "name": "LIGHTS",
            "type": "output",
            "mode": "analog",
            "status": "low",
            "value": 251,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_4",
            "name": "AIR CONDITIONAT",
            "type": "output",
            "mode": "analog",
            "status": "low",
            "value": 237,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_5",
            "name": "UMIDITATE ",
            "type": "input",
            "mode": "analog",
            "status": "off",
            "value": 130,
            "active": False,
            "active_web": "active"
        },
        {
            "id": "sensor_6",
            "name": "TEMPERATURA",
            "type": "input",
            "mode": "analog",
            "status": "off",
            "value": 154,
            "active": False,
            "active_web": "active"
        },
        {
            "id": "sensor_7",
            "name": "Sensor 7",
            "type": "input",
            "mode": "digital",
            "status": "off",
            "value": 0,
            "active": False,
            "active_web": "inactive"
        },
        {
            "id": "sensor_8",
            "name": "PIN_2_ORANGE",
            "type": "input",
            "mode": "digital",
            "status": "low",
            "value": 0,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_9",
            "name": "PIN_1_BLUE",
            "type": "input",
            "mode": "digital",
            "status": "low",
            "value": 0,
            "active": True,
            "active_web": "active"
        },
        {
            "id": "sensor_10",
            "name": "Sensor 10",
            "type": "input",
            "mode": "digital",
            "status": "off",
            "value": 68,
            "active": False,
            "active_web": "inactive"
        }
    ]

    db["sensors"].delete_many({})  # Reset the collection
    db["sensors"].insert_many(default_sensors)  # Insert default sensors





@csrf_exempt
@login_required
@user_passes_test(superuser_required)
def reset_sensors(request):
    """Reset all sensors to default state."""
    if request.method == 'POST':
        try:
            initialize_sensors()
            return JsonResponse({"message": "Sensors reset successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)


    
@csrf_exempt
def receive_data(request):
    """Receive sensor data from POST requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for sensor_id, value in data.items():
                sensor = db["sensors"].find_one({"id": sensor_id})
                if not sensor:
                    continue
                update = {}
                if isinstance(value, int):
                    update["value"] = value
                    update["status"] = "high" if value else "low"
                elif value in ["high", "low"]:
                    update["status"] = value
                    update["value"] = 1 if value == "high" else 0
                db["sensors"].update_one({"id": sensor_id}, {"$set": update})
            return JsonResponse({"message": "Data received"}, status=200)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def send_command(request):
    """Send commands to sensors like 'high', 'low', or analog values."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            command = data.get("command")
            value = data.get("value")

            sensor = db["sensors"].find_one({"id": sensor_id})
            if not sensor:
                return JsonResponse({"error": "Sensor not found"}, status=400)

            update = {}
            if command in ["high", "low"] and sensor["mode"] == "digital":
                update["status"] = command
            elif command == "set_value" and sensor["mode"] == "analog":
                update["value"] = value
            db["sensors"].update_one({"id": sensor_id}, {"$set": update})

            return JsonResponse({"message": "Command sent successfully"}, status=200)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@csrf_exempt
def configure_sensor(request):
    """Configure sensor attributes."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get("sensor_id")
            sensor = db["sensors"].find_one({"id": sensor_id})
            if not sensor:
                return JsonResponse({"error": "Sensor not found"}, status=400)

            update = {}
            for key in ["name", "type", "mode", "active"]:
                if key in data:
                    update[key] = data[key]

            db["sensors"].update_one({"id": sensor_id}, {"$set": update})
            return JsonResponse({"message": "Configuration updated successfully"}, status=200)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

@user_passes_test(superuser_required)
@login_required
def control_page(request):
    """Render control page for Arduino."""
    initialize_sensors()
    sensors = list(db["sensors"].find())  # Fetch all sensors
    return render(request, 'arduino_comm/control_panel.html', {"device_status": sensors})

@csrf_exempt
def save_sensors(request):
    """Save data for multiple sensors."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for sensor_data in data.get("sensors", []):
                sensor_id = sensor_data.get("sensor_id")
                update = {k: sensor_data[k] for k in ["name", "type", "mode", "active", "value", "status"] if k in sensor_data}
                db["sensors"].update_one({"id": sensor_id}, {"$set": update}, upsert=True)

            return JsonResponse({"message": "All sensors updated successfully"}, status=200)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({"error": "Invalid JSON or Sensor not found"}, status=400)
    return JsonResponse({"error": "Only POST requests are accepted"}, status=400)

def fetch_sensor_data(request):
    """Fetch current status of all sensors."""
    sensors = list(db["sensors"].find())
    data = {sensor["id"]: {
        "name": sensor["name"],
        "type": sensor["type"],
        "mode": sensor["mode"],
        "status": sensor["status"],
        "value": sensor["value"],
        "active": sensor["active"]
    } for sensor in sensors}
    return JsonResponse(data)

def active_sensors_page(request):
    """Render page displaying only active sensors."""
    initialize_sensors()
    sensors = list(db["sensors"].find({"active": True}))
    return render(request, 'arduino_comm/active_sensors.html', {"device_status": sensors})
