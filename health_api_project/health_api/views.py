from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HealthRecord
from .serializers import HealthRecordSerializer

@api_view(['GET'])
def get_health_records(request):
    health_records = HealthRecord.objects.all()
    serializer = HealthRecordSerializer(health_records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_health_record(request):
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def health_record_detail(request, pk):
    try:
        health_record = HealthRecord.objects.get(pk=pk)
    except HealthRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HealthRecordSerializer(health_record)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = HealthRecordSerializer(health_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        health_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
