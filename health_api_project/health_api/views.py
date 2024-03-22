from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import HealthRecord
from .serializers import HealthRecordSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_records(request):
    user = request.user
    if request.user.is_superuser:
        health_records = HealthRecord.objects.all()
    else:
        health_records = HealthRecord.objects.filter(user=user)
    serializer = HealthRecordSerializer(health_records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_health_record(request):
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def health_record_detail(request, pk):
    try:
        health_record = HealthRecord.objects.get(pk=pk)
        if health_record.user != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
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

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error' : 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def token_obtain_pair_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = User.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })