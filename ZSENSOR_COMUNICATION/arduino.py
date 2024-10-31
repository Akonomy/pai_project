import serial
import requests
import time
import json

# Configure the serial port for the Arduino
PORT = "COM11"  # Update if using a different port
BAUDRATE = 9600
ARDUINO_TIMEOUT = 2

# Django server configuration
DJANGO_FETCH_URL = "http://127.0.0.1:8000/fetch/"  # Django API endpoint to fetch data
DJANGO_UPDATE_URL = "http://127.0.0.1:8000/receive/"  # Django API endpoint to receive sensor updates

# Initialize serial communication if available
arduino_serial = None
try:
    arduino_serial = serial.Serial(PORT, BAUDRATE, timeout=ARDUINO_TIMEOUT)
    if arduino_serial.is_open:
        print(f"Serial port {PORT} opened successfully.")
except serial.SerialException as e:
    print("Warning: Could not open serial port. Running in simulation mode.")
    arduino_serial = None

def fetch_data_from_django():
    """Fetch latest sensor data from Django API and display it."""
    try:
        response = requests.get(DJANGO_FETCH_URL)
        if response.status_code == 200:
            sensor_data = response.json()
            print("Current sensor data from Django:")
            for sensor_id, data in sensor_data.items():
                if data["active"]:  # Only consider active sensors
                    print(f"  {sensor_id}: {data}")
            return {k: v for k, v in sensor_data.items() if v["active"]}  # Return active sensors only
        else:
            print("Failed to fetch data:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Django:", e)
    return {}

def send_command_to_arduino(command):
    """Send command to Arduino directly."""
    if arduino_serial:
        try:
            arduino_serial.write((command + "\n").encode('utf-8'))
            print("Sent command to Arduino:", command)
        except Exception as e:
            print("Error sending command to Arduino:", e)


    """Send sensor data to Django API."""
def send_data_to_django(sensor_data):
    # Map 'high'/'low' to integers
    value_mapping = {'high': 1, 'low': 0}
    processed_data = {}
    for key, value in sensor_data.items():
        if value in value_mapping:
            processed_data[key] = value_mapping[value]
        else:
            processed_data[key] = value  # Assuming it's already an integer
    try:
        response = requests.post(DJANGO_UPDATE_URL, json=processed_data)
        if response.status_code == 200:
            print("Data sent successfully:", sensor_data)
        else:
            print("Failed to send data:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending data to Django:", e)

def read_from_arduino():
    """Read data from Arduino and process sensor_8 and sensor_9 states."""
    if arduino_serial and arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode('utf-8').strip()
            print("Received data from Arduino:", data)
            # Parse JSON data
            try:
                json_data = json.loads(data)
                if "sensor_8" in json_data or "sensor_9" in json_data:
                    send_data_to_django(json_data)  # Send data to Django only if relevant
            except json.JSONDecodeError:
                print("Invalid JSON format received from Arduino.")
        except Exception as e:
            print("Error reading from Arduino:", e)

def main():
    print("Starting Arduino to Web communication...")
    while True:
        # Read from Arduino for input states
        read_from_arduino()
        
        # Fetch and handle active sensors from Django
        django_data = fetch_data_from_django()

        if django_data:
            for sensor_id, data in django_data.items():
                if sensor_id == "sensor_1" or sensor_id == "sensor_2":  # Digital-only sensors
                    if data["mode"] == "digital":
                        command = f"{sensor_id}_{data['status']}"
                    else:
                        command = f"{sensor_id}_{'high' if data['value'] > 127 else 'low'}"
                    send_command_to_arduino(command)

                elif sensor_id == "sensor_3" or sensor_id == "sensor_4":  # Supports both digital and analog
                    if data["mode"] == "analog":
                        command = f"{sensor_id}_value_{data['value']}"
                    else:
                        command = f"{sensor_id}_{data['status']}"
                    send_command_to_arduino(command)

        time.sleep(1)

if __name__ == "__main__":
    main()
