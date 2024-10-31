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

# Configure the serial port for the Arduino
PORT = "COM11"  # Update if using a different port
BAUDRATE = 9600
ARDUINO_TIMEOUT = 2

# Django server configuration
DJANGO_RECEIVE_URL = "http://127.0.0.1:8000/receive/"  # Django API endpoint to receive sensor data
DJANGO_FETCH_URL = "http://127.0.0.1:8000/fetch/"  # Django API endpoint to fetch data

# Try to initialize serial communication, if enabled
arduino_serial = None
if SERIAL_ENABLED:
    try:
        arduino_serial = serial.Serial(PORT, BAUDRATE, timeout=ARDUINO_TIMEOUT)
        if arduino_serial.is_open:
            print(f"Serial port {PORT} opened successfully.")
    except serial.SerialException as e:
        print("Warning: Could not open serial port. Running in simulation mode.")
        SERIAL_ENABLED = False

def read_from_serial():
    """Read a line of data from Arduino via serial, if serial is enabled."""
    if SERIAL_ENABLED and arduino_serial and arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode('utf-8').strip()
            print(f"Received data from Arduino: {data}")  # Debug: show received data
            return data
        except Exception as e:
            print("Error reading from serial:", e)
    return None

def fetch_data_from_django():
    """Fetch latest sensor data from Django API and display it."""
    try:
        response = requests.get(DJANGO_FETCH_URL)
        if response.status_code == 200:
            sensor_data = response.json()
            print("Current sensor data from Django:")
            for sensor_id, data in sensor_data.items():
                print(f"  {sensor_id}: {data}")
            return sensor_data
        else:
            print("Failed to fetch data:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Django:", e)
    return None

def send_command_to_arduino(command):
    """Send command to Arduino directly."""
    if SERIAL_ENABLED:
        try:
            arduino_serial.write((command + "\n").encode('utf-8'))
            print("Sent command to Arduino:", command)
        except Exception as e:
            print("Error sending command to Arduino:", e)

def main():
    print("Starting Arduino to Web communication...")
    while True:
        django_data = fetch_data_from_django()

        if django_data:
            for sensor_id, data in django_data.items():
                if sensor_id == "sensor_1":
                    # Send high/low command for sensor_1
                    command = f"{sensor_id}_{data['status']}"
                    send_command_to_arduino(command)
                elif sensor_id == "sensor_2":
                    # Send high/low command for sensor_2
                    command = f"{sensor_id}_{data['status']}"
                    send_command_to_arduino(command)
                elif sensor_id == "sensor_3":
                    # Send PWM value for sensor_3
                    command = f"{sensor_id}_value_{data['value']}"
                    send_command_to_arduino(command)

        # Wait before the next iteration
        time.sleep(1)

if __name__ == "__main__":
    main()
