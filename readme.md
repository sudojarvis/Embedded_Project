Install xgboost and djangorestframework

 1. sudo pip install xgboost
 2. pip install djangorestframework

Before running arduino code
    
     1. Change the ssid and password to your wifi network.
     2. Change the ip address to the ip address of your computer.
     3. Change the port to the port you want to use.
        go to utils.py and change the port to the same port you used in the arduino code.

Go to file->preferences and add below url in the "Additional Boards Manager URLs" field.
```
http://arduino.esp8266.com/stable/package_esp8266com_index.json
```
Then go to Tools->Board->Boards Manager and search for esp8266 and install it.

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


## 4. Upload the code
Connect your ESP8266 to your computer and upload the code. If you have any issues,contact me.

To run the django server

1. clone the repository
2. cd mysite
3. python manage.py runserver

go to http://localhost:8000/sensordata/ to start sensor data being stored in the database.

go to http://localhost:8000/home/ to forecast temperature, humidity and and water level.
Enter the 24 hour format of the time you want to predict for and click on submit.
