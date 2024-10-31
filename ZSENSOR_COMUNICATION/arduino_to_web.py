import requests
import time
import random
import json

try:
    import serial
    SERIAL_ENABLED = True
except ImportError:
    print("Serial library not available; running in simulation mode.")
    SERIAL_ENABLED = False

# Configure the serial port for the Arduino (optional)
PORT = "COM3"  # Change this if using Arduino with serial
BAUDRATE = 9600
ARDUINO_TIMEOUT = 2

# Django server configuration
DJANGO_SERVER_URL = "http://127.0.0.1:8000/receive/"  # Django API endpoint

# Try to initialize serial communication, if enabled
arduino_serial = None
if SERIAL_ENABLED:
    try:
        arduino_serial = serial.Serial(PORT, BAUDRATE, timeout=ARDUINO_TIMEOUT)
    except serial.SerialException as e:
        print("Warning: Could not open serial port. Running in simulation mode.")
        SERIAL_ENABLED = False

# Simulated sensor state for sensor_8, sensor_9, and sensor_10
simulated_sensors = {
    "sensor_8": 0,
    "sensor_9": 0,
    "sensor_10": 0
}

def read_from_serial():
    """Read a line of data from Arduino via serial, if serial is enabled."""
    if SERIAL_ENABLED and arduino_serial and arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode('utf-8').strip()
            return data
        except Exception as e:
            print("Error reading from serial:", e)
    return None

def send_data_to_django(sensor_data):
    """Send sensor data to Django API."""
    try:
        response = requests.post(DJANGO_SERVER_URL, json=sensor_data)
        if response.status_code == 200:
            print("Data sent successfully:", sensor_data)
        else:
            print("Failed to send data:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending data to Django:", e)

def simulate_sensor_data():
    """Simulate sensor data for sensor_8, sensor_9, and sensor_10."""
    for sensor in simulated_sensors:
        # Generate random rise and fall within a specified range
        simulated_sensors[sensor] += random.randint(-150, 150)
        simulated_sensors[sensor] = max(0, min(100, simulated_sensors[sensor]))  # Keep within 0-100 range
    return simulated_sensors

def main():
    print("Starting Arduino to Web communication...")
    while True:
        # Step 1: Read data from Arduino if available
        arduino_data = read_from_serial()
        sensor_data = {}

        if arduino_data:
            try:
                # Expect Arduino data in JSON format (e.g., {"sensor_1": 25, "sensor_2": 30})
                sensor_data = json.loads(arduino_data)
            except json.JSONDecodeError:
                print("Invalid data format from Arduino:", arduino_data)
        
        # Step 2: Simulate data for sensor_8, sensor_9, and sensor_10 if no serial data
        simulated_data = simulate_sensor_data()
        sensor_data.update(simulated_data)

        # Step 3: Send data to Django server if there's any sensor data
        if sensor_data:
            send_data_to_django(sensor_data)

        # Wait for a while before the next reading
        time.sleep(5)

if __name__ == "__main__":
    main()
