import serial

import datetime

PORT="/dev/ttyUSB1"

BAUD=9600

ser = serial.Serial(PORT, BAUD)

import json


while True:

    line = ser.readline().decode('utf-8')
    # line.get("temperature")
    # print(line.get("temperature"))
    if line.startswith('{'):
        data = json.loads(line)
        # print(data)
        # print(data.get("temperature"))


        # print(line)