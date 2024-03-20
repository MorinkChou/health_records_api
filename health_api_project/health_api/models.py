from django.db import models
from django.contrib.auth.models import User

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    blood_pressure = models.FloatField()
    heart_rate = models.IntegerField()
    blood_sugar = models.FloatField()
    date = models.DateField(auto_now_add=True)