from django.db import models
from django.utils import timezone

# Create your models here.
class SensorData(models.Model):
    timestamp = models.CharField(max_length=100)
    temperature = models.CharField(max_length=100, null=True)
    humidity = models.CharField(max_length=100, null=True)
    water_level = models.CharField(max_length=100, null=True)
    hour= models.CharField(max_length=100, null=True)
    minutes= models.CharField(max_length=100, null=True)
    seconds= models.CharField(max_length=100, null=True)
    django_time = models.DateTimeField(null=True)
