from django.urls import path
from . import views

urlpatterns = [
    path('', views.sensorData,name='sensorData'),
    #path('', views.train,name='train')
    path('', views.home_view, name='home'),
    # path('', views.train_loop, name='train'),
]


