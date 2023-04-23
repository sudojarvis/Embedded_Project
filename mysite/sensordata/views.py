from django.shortcuts import render

# Create your views here.
# from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import SensorData

from .utility import store_data

import json

# import concurrent.futures

import pandas as pd
from .utility import predict, load_model #, normalize_data


import threading


def sensorData(request):
    if not hasattr(sensorData, "thread") or not sensorData.thread.is_alive():
        sensorData.thread = threading.Thread(target=store_data)
        sensorData.thread.daemon = True
        sensorData.thread.start()
    return HttpResponse("Data is being stored")


from rest_framework.decorators import api_view
from .form import InputForm
# @csrf_exempt
# def home_view(request):
#     context = {}
#     if request.method == "POST":
#         form = InputForm(request.POST)
#         if form.is_valid():
#             hour = form.cleaned_data['hour']
#             minutes = form.cleaned_data['minutes']
#             seconds = form.cleaned_data['seconds']
#             print(hour,minutes,seconds)
#             context['hour'] = hour
#             context['minutes'] = minutes
#             context['seconds'] = seconds
#             return render(request, 'home.html', context)

#     else:
#         form = InputForm()
#         return render(request, 'home.html', {'form': form}) 
        
@csrf_exempt


def home_view(request):
    context = {}

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            hour = form.cleaned_data['hour']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']

            data=pd.DataFrame({'hour':[hour],'minutes':[minutes],'seconds':[seconds]})
          
            model_temp = load_model('model_temp.pkl')
            model_hum = load_model('model_hum.pkl')
            model_water = load_model('model_water.pkl')
            # normalize_data(data)
            predict_temp = predict(model_temp, data)
            predict_hum = predict(model_hum, data)
            predict_water = predict(model_water, data)

            context['form'] = form
            context['hour'] = hour
            context['minutes'] = minutes
            context['seconds'] = seconds
            context['predict_water_level'] = predict_water
            context['predict_temperature'] = predict_temp
            context['predict_humidity'] = predict_hum

            return render(request, 'home.html', context)
    else:
        form = InputForm()
        context['form'] = form

    return render(request, 'home.html', context)

