#include <ArduinoJson.h>  // Include ArduinoJson library

// Pin Definitions
const int ledPins[] = {2, 3, 5, 6};  // LEDs for command control
const int inputPin12 = 12;           // Input pin for sensor_8
const int inputPin13 = 13;           // Input pin for sensor_9
int lastState12 = LOW;               // Last state of pin 12
int lastState13 = LOW;               // Last state of pin 13

void setup() {
  // Initialize LED pins as output
  for (int i = 0; i < 4; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  
  // Initialize input pins
  pinMode(inputPin12, INPUT);
  pinMode(inputPin13, INPUT);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Check for incoming commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the incoming command until newline

    // Command handling for LEDs on pins 2, 3, 5, and 6
    if (command == "sensor_1_high") {
      digitalWrite(2, HIGH);
    }
    else if (command == "sensor_1_low") {
      digitalWrite(2, LOW);
    }
    else if (command == "sensor_2_high") {
      digitalWrite(3, HIGH);
    }
    else if (command == "sensor_2_low") {
      digitalWrite(3, LOW);
    }
    else if (command == "sensor_3_high") {
      digitalWrite(5, HIGH);
    }
    else if (command == "sensor_3_low") {
      digitalWrite(5, LOW);
    }
    else if (command == "sensor_4_high") {
      digitalWrite(6, HIGH);
    }
    else if (command == "sensor_4_low") {
      digitalWrite(6, LOW);
    }
    else if (command.startsWith("sensor_3_value_")) {
      int pwmValue = command.substring(15).toInt();  // Extract PWM value after "sensor_3_value_"
      analogWrite(5, pwmValue);
    }
    else if (command.startsWith("sensor_4_value_")) {
      int pwmValue = command.substring(15).toInt();  // Extract PWM value after "sensor_4_value_"
      analogWrite(6, pwmValue);
    }
  }

  // Check the state of input pins and send updates if their state changes
  int currentState12 = digitalRead(inputPin12);
  int currentState13 = digitalRead(inputPin13);

  if (currentState12 != lastState12) {
    lastState12 = currentState12;
    String stateMessage = String("{\"sensor_8\": ") + (currentState12 == HIGH ? "\"high\"" : "\"low\"") + "}";
    Serial.println(stateMessage);
  }

  if (currentState13 != lastState13) {
    lastState13 = currentState13;
    String stateMessage = String("{\"sensor_9\": ") + (currentState13 == HIGH ? "\"high\"" : "\"low\"") + "}";
    Serial.println(stateMessage);
  }

  delay(100);  // Small delay to avoid spamming the serial buffer
}
