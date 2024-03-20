from django.urls import path
from . import views

urlpatterns = [
    path('health-records/', views.get_health_records, name='health_records_list'),
    path('health-records/create/', views.create_health_record, name='create_health_record'),
    path('health-records/<int:pk>/', views.health_record_detail, name='health_record_detail'),
]
