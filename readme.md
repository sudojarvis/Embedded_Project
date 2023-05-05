## Arduino IDE setup For NodeMCU

Go to file->preferences and add below url in the "Additional Boards Manager URLs" field.

```
http://arduino.esp8266.com/stable/package_esp8266com_index.json
```

Then go to Tools->Board->Boards Manager and search for esp8266 and install it.

## Hardware connection Required

For DHT11 sensor:

1. connect the VCC of DHT sensor to Vin of NodeMCU
2. connect the GND of DHT sensor to GND of NodeMCU
3. connect the data pin of DHT sensor to D3 of NodeMCU

For Water level sensor:

1. Connect the Signal pin(S) of water level sensor to A0 of NodeMCU
2. Connect the VCC of water level sensor to Vin of NodeMCU
3. Connect the GND of water level sensor to GND of NodeMCU

## 2. Install the required libraries in Arduino IDE if you don't have them already

Go to Sketch->Include Library->Manage Libraries and install the following libraries:

- Adafruit Unified Sensor
- Adafruit BME280 Library
- Adafruit_BusIO
- AnalogRTCLib
- Arduino_AdvancedAnalog
- ArduinoJson
- DHT sensor library
- ESP8266WiFi
- ESP8266HTTPClient
- RTClib
- NTPClient
- Time

## Upload the code

- connect the USB cable to the computer and upload the code to the NodeMCU using Arduino IDE.
- Select the board as NodeMCU 0.9 (ESP-12E Module) and the port to which the NodeMCU is connected to the computer.

## Before running arduino code

1. Change the ssid and password to your wifi network.
2. Change the ip address to the ip address of your computer.
3. Change the port to the port you want to use.
go to utils.py and change the port to the same port you used in the arduino code.

## Installation and setup required for Django server and ML model

### To run Django server and ML model

1. clone the repository
2. cd mysite
3. Install xgboost,django and djangorestframework
   1. `pip install Django==4.2.1`
   2. `sudo pip install xgboost`
   3. `pip install djangorestframework`

4. run `python manage.py runserver`

- go to http://localhost:8000/sensordata/ to start sensor data being stored in the database.

- go to http://localhost:8000/home/ to forecast temperature, humidity and and water level.
Enter the 24 hour format of the time you want to predict for and click on submit.
