import serial

# import datetime

from django.utils import timezone
import os

import pytz
# from datetime import datetime

# create a datetime object in a specific timezone
# tz = pytz.timezone('Asia/Kolkata')
# dt = datetime.now(tz)

PORT="/dev/ttyUSB0"

BAUD=9600



ser = serial.Serial(PORT, BAUD)

from .models import SensorData

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django

django.setup()

import json

from datetime import datetime, timedelta

def delete_old_data():
    keep_date = datetime.now() - timedelta(days=3)
    old_data = SensorData.objects.filter(django_time__lt=keep_date)
    old_data.delete()

def delele_all_data():
    SensorData.objects.all().delete()

# delele_all_data()

def store_data():

    while True:

        line = ser.readline().decode('utf-8')
        # line.get("temperature")
        # print(line.get("temperature"))
        tz = pytz.timezone('Asia/Kolkata')
        dt = datetime.now(tz)
        if line.startswith('{'):
            data = json.loads(line)
            # print(data)
            # print(data.get("temperature"))
            # new_time_ = timezone.now()
            now = datetime.now()
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            water_level = data.get('water_level')
            hour = data.get('hours')
            minutes = data.get('minutes')
            seconds = data.get('seconds')
            timestamp = data.get('formattedTime')
            sensor_data=SensorData.objects.create(
                temperature=temperature,
                humidity=humidity,
                water_level=water_level,
                hour=hour,
                minutes=minutes,
                seconds=seconds,
                timestamp=timestamp,
                # django_time=timezone.make_aware(now, timezone.utc)
                django_time=dt
            
            )

            # print("Temperature: ", temperature)

            sensor_data.save()
            # print("Temperature: ", temperature)
            print("successfully saved data to db")
            # delete_old_data()
            # delele_all_data()
            # # break

import pandas as pd

def get_data_from_db():
    data = SensorData.objects.all()
    df= pd.DataFrame(data.values(), columns=['id','timestamp','temperature','humidity','water_level','hour','minutes','seconds','django_time'])
    # print(data[0]._meta.get_fields())
    # df=df.drop(['id','timestamp','django_time'],axis=1)
    return df

# print(get_data_from_db().head())

from sklearn.preprocessing import MinMaxScaler
    # scaler = MinMaxScaler()
def preprocess_data(data):
    # scaler = MinMaxScaler()
    df=data.drop(['id','timestamp','django_time'],axis=1)
    df=df.astype('float')
    # df['hour'] = scaler.fit_transform(df[['hour']])
    # df['minutes'] = scaler.fit_transform(df[['minutes']])
    # df['seconds'] = scaler.fit_transform(df[['seconds']])
    df_temp=df[['hour','minutes','seconds','temperature']]
    df_hum=df[['hour','minutes','seconds','humidity']]
    df_water=df[['hour','minutes','seconds','water_level']]

    return df_temp,df_hum,df_water

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# def normalize_data(df):
#     scaler = MinMaxScaler()
#     df['hour'] = scaler.fit_transform(df[['hour']])
#     df['minutes'] = scaler.fit_transform(df[['minutes']])
#     df['seconds'] = scaler.fit_transform(df[['seconds']])

def model():
    df=get_data_from_db()
    df_temp,df_hum,df_water=preprocess_data(df)
    # normalize_data(df_temp)
    X_temp=df_temp.drop(['temperature'],axis=1)
    y_temp=df_temp['temperature']
    X_hum=df_hum.drop(['humidity'],axis=1)
    y_hum=df_hum['humidity']
    X_water=df_water.drop(['water_level'],axis=1)
    y_water=df_water['water_level']
    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)
    X_train_hum, X_test_hum, y_train_hum, y_test_hum = train_test_split(X_hum, y_hum, test_size=0.2, random_state=42)
    X_train_water, X_test_water, y_train_water, y_test_water = train_test_split(X_water, y_water, test_size=0.2, random_state=42)
    reg_temp=xgb.XGBRegressor(n_estimators=1000,learning_rate=0.001,booster='gbtree',max_depth=20)
    reg_hum=xgb.XGBRegressor(n_estimators=1000,learning_rate=0.001,booster='gbtree',max_depth=20)
    reg_water=xgb.XGBRegressor(n_estimators=1000,learning_rate=0.001,booster='gbtree',max_depth=20)
    reg_temp.fit(X_train_temp,y_train_temp,verbose=False)
    reg_hum.fit(X_train_hum,y_train_hum,verbose=False)
    reg_water.fit(X_train_water,y_train_water,verbose=False)

    def accuracy(model,X_test,y_test):
        predictions=model.predict(X_test)
        # from sklearn.metrics import mean_squared_error
        print("Mean Absolute Error : " + str(mean_squared_error(predictions, y_test))) 
    accuracy(reg_temp,X_test_temp,y_test_temp)
    accuracy(reg_hum,X_test_hum,y_test_hum)
    accuracy(reg_water,X_test_water,y_test_water)


    return reg_temp,reg_hum,reg_water

def save_model(model, filename):
    import pickle
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print("Model saved successfully")



def load_model(filename):
    import pickle
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

def predict(model, data):
    prediction = model.predict(data)
    return prediction



# model_temp,model_hum,model_water=model()
# save_model(model_temp, 'model_temp.pkl')
# save_model(model_hum, 'model_hum.pkl')
# save_model(model_water, 'model_water.pkl')

def train_model():
    model_temp,model_hum,model_water=model()
    save_model(model_temp, 'model_temp.pkl')
    save_model(model_hum, 'model_hum.pkl')
    save_model(model_water, 'model_water.pkl')
    return model_temp,model_hum,model_water




#plotting the graph for next 24 hours
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt
# import numpy as np
# from matplotlib import style

import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_graph():
    now=datetime.now()
    hour=now.hour
    # minutes=now.minute
    # seconds=now.second
    hour_data=[]
    for i in range(24):
        hour_data.append(hour)
        hour=(hour+1)%24
       
    min_data=random.sample(range(0, 60), 24)
    sec_data=random.sample(range(0, 60), 24)

    # print(hour_data)
    # print(min_data)
    # print(sec_data)



    hourly_data=pd.DataFrame()
    hourly_data['hour']=hour_data

    hourly_data['minutes']=min_data
    hourly_data['seconds']=sec_data
    hourly_data['hour']=hourly_data['hour'].astype('int')
    hourly_data['minutes']=hourly_data['minutes'].astype('int')
    hourly_data['seconds']=hourly_data['seconds'].astype('int')
    hourly_data['time']=hourly_data['hour'].astype('str')+":"+hourly_data['minutes'].astype('str')+":"+hourly_data['seconds'].astype('str')
    hourly_data['time']=pd.to_datetime(hourly_data['time'],format='%H:%M:%S')

    model_temp=load_model('model_temp.pkl')
    model_hum=load_model('model_hum.pkl')
    model_water=load_model('model_water.pkl')
    temp_pred=model_temp.predict(hourly_data[['hour','minutes','seconds']])
    hum_pred=model_hum.predict(hourly_data[['hour','minutes','seconds']])
    water_pred=model_water.predict(hourly_data[['hour','minutes','seconds']])
    hourly_data['temperature']=temp_pred
    hourly_data['humidity']=hum_pred
    hourly_data['water_level']=water_pred
    hourly_data['hour']=hourly_data['hour'].astype('int')
    hourly_data['minutes']=hourly_data['minutes'].astype('int')
    hourly_data['seconds']=hourly_data['seconds'].astype('int')

    hourly_data['time']=hourly_data['hour'].astype('str')+":"+hourly_data['minutes'].astype('str')+":"+hourly_data['seconds'].astype('str')
    # hourly_data['time']=pd.to_datetime(hourly_data['time'],format='%H:%M:%S')
    # print(hourly_data['time'])


    # hourly_data['time']=hourly_data['hour'].astype('str')+":"+hourly_data['minutes'].astype('str')+":"+hourly_data['seconds'].astype('str')
    # hourly_data['time']=pd.to_datetime(hourly_data['time'],format='%H:%M:%S')
    hourly_data=hourly_data.drop(['hour','minutes','seconds'],axis=1)
    hourly_data=hourly_data.set_index('time')
    # hourly_data=hourly_data.astype('float')
    # hourly_data.plot()
    graph=hourly_data.plot()
    graph.set_xlabel("Time")

    plt.legend(loc='best')
    plt.title("Prediction for next 24 hours")

    plt.savefig('data.png')
    

    # plt.show()
    plt.clf()

# plot_graph()



import threading

import time
def schedule_model_training():
   while(True):
         threading.Timer(60.0, train_model).start()
        #  threading.Timer(60.0, plot_graph).start()
         time.sleep(60)
         print("Model Trained")






def schedule_plotting():
    while(True):
            threading.Timer(60.0, plot_graph).start()
            time.sleep(60)
            print("Graph plotted")


t1=threading.Thread(target=schedule_plotting)
t2=threading.Thread(target=schedule_model_training)
t1.start()
t2.start()
# t1.join()
# t2.join()

# t=threading.Thread(target=schedule_model_training)
# t.start()


# #plotting the graph for next 24 hours
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt
# import numpy as np
# from matplotlib import style

# import random
# def plot_graph():
#     now=datetime.now()
#     hour=now.hour
#     minutes=now.minute
#     seconds=now.second
#     hourly_data=[]

#     min_data=random.sample(range(minutes, 60), 24)
#     sec_data=random.sample(range(seconds, 60), 24)
#     for i in range(24):
#         hourly_data.append([hour,min_data[i],sec_data[i]])
#     hourly_data=np.array(hourly_data)
#     hourly_data=hourly_data.reshape(24,3)
#     hourly_data=pd.DataFrame(hourly_data,columns=['hour','minutes','seconds'])
#     hourly_data=hourly_data.astype('float')

#     model_temp=load_model('model_temp.pkl')
#     model_hum=load_model('model_hum.pkl')
#     model_water=load_model('model_water.pkl')
#     temp_pred=model_temp.predict(hourly_data)
#     hum_pred=model_hum.predict(hourly_data)
#     water_pred=model_water.predict(hourly_data)
#     hourly_data['temperature']=temp_pred
#     hourly_data['humidity']=hum_pred
#     hourly_data['water_level']=water_pred
#     hourly_data['hour']=hourly_data['hour'].astype('int')
#     hourly_data['minutes']=hourly_data['minutes'].astype('int')
#     hourly_data['seconds']=hourly_data['seconds'].astype('int')
#     hourly_data['time']=hourly_data['hour'].astype('str')+":"+hourly_data['minutes'].astype('str')+":"+hourly_data['seconds'].astype('str')
#     hourly_data['time']=pd.to_datetime(hourly_data['time'],format='%H:%M:%S')
#     hourly_data=hourly_data.drop(['hour','minutes','seconds'],axis=1)
#     hourly_data=hourly_data.set_index('time')
#     hourly_data=hourly_data.astype('float')
#     hourly_data.plot()
#     plt.show()

# plot_graph()






    
    





   






