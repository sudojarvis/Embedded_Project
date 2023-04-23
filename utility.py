from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

import json

import datetime

import serial

PORT="/dev/ttyUSB1"

BAUD=9600

ser = serial.Serial(PORT, BAUD)

engine = create_engine('mysql://root:root@localhost:8001/mydatabase')

Session = sessionmaker(bind=engine)

class SensorData(Base):
    __tablename__='sensordata'
    id = Column(Integer, primary_key=True)
    timpestamp = Column(String(100))
    temperature =Column(Float)
    humidity = Column(Float)
    water_level = Column(Float)
    hour= Column(Integer)
    minutes= Column(Integer)
    seconds= Column(Integer)
    django_time = Column(DateTime)
    


with Session() as session:
    while True:

        line = ser.readline().decode('utf-8')
        # line.get("temperature")
        # print(line.get("temperature"))
        if line.startswith('{'):
            data = json.loads(line)
            # print(data)
            # print(data.get("temperature"))
            sensor_data=SensorData(
                timpestamp=data.get("timpestamp"),
                temperature=data.get("temperature"),
                humidity=data.get("humidity"),
                water_level=data.get("water_level"),
                hour=data.get("hour"),
                minutes=data.get("minutes"),
                seconds=data.get("seconds"),
                django_time=data.get("django_time")
            )

            session.add(sensor_data)
            session.commit()


