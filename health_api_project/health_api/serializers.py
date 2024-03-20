from rest_framework import serializers
from .models import HealthRecord

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'user', 'weight', 'blood_pressure', 'heart_rate', 'blood_sugar', 'date']