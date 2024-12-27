# PAI_Project

## Overview

This project is a Django-based web application that integrates with an Arduino for automating home utilities such as lights and air conditioning. The project simulates control through a web interface and provides feedback on the status of connected devices.

### Key Components

#### 1. `PAI_APP/`
This folder contains the main Django configuration files:
- **`settings.py`**: Global settings for database, static files, and installed apps.
- **`urls.py`**: Routes that connect URLs to views across the project.
- **`wsgi.py`**: Configuration for running the application on WSGI servers.

#### 2. `apps/`
Contains the individual Django apps that encapsulate distinct functionalities:
- **`main/`**: Manages user-related functionality such as login, registration, and the dashboard.
  - Contains templates for user-facing pages like `login.html`, `register.html`, and `dashboard.html`.
- **`arduino_comm/`**: Focused on communication with the Arduino and sensor configurations.
  - Provides REST APIs for sending and receiving data to/from the Arduino.

#### 3. `static/`
Includes resources for the web interface:
- **`css/`**: Styling files.
- **`js/`**: JavaScript for interactivity.
- **`images/`**: Visual assets for the UI.

#### 4. `templates/`
HTML templates for the application:
- **`main/`**: Login, profile, and dashboard pages.
- **`arduino_comm/`**: Pages for managing sensors and controls.

#### 5. `ZSENSOR_COMUNICATION/`
This folder contains scripts for Arduino integration:
- **`arduino.py`**: Handles serial communication with the Arduino.
- **`arduino_script.ino`**: The Arduino firmware for managing sensors and devices.
- **`simulator.py`**: A Python-based simulator for testing without physical hardware.

#### 6. Other Important Files
- **`manage.py`**: Django management script for running the server and managing migrations.
- **`requirements.txt`**: List of dependencies needed for the project.
- **`db.sqlite3`**: SQLite database file for storing project data.

---

## Getting Started

### Prerequisites
Make sure you have the following installed on your machine:
- Python 3.9 or later
- pip (Python package installer)
- Git
- Arduino IDE (optional, for uploading firmware to the Arduino board)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Akonomy/pai_project.git
   cd pai_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate

   # On Linux/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up the admin account.

6. Run the development server:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000`.

### Configuring Arduino
1. Open `ZSENSOR_COMUNICATION/arduino_script.ino` in the Arduino IDE.
2. Connect your Arduino board and upload the script.
3. Ensure the port settings in `arduino.py` match the connected port.

---

## Usage
- **Login/Registration**: Access user accounts and the dashboard.
- **Dashboard**: Control devices and monitor their status.
- **Control Sensors**: Use the `arduino_comm` API to configure and interact with sensors.

### API Endpoints
- **`/fetch/`**: Fetch current sensor data.
- **`/receive/`**: Send updates to sensors.

---

## Troubleshooting
- **Missing Dependencies**:
  Ensure all libraries are installed using:
  ```bash
  pip install -r requirements.txt
  ```
- **Port Issues with Arduino**:
  Check the connected port using:
  ```bash
  python -m serial.tools.list_ports
  ```
- **Database Issues**:
  If migrations fail, delete `db.sqlite3` and rerun:
  ```bash
  python manage.py migrate
  ```

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
