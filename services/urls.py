from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('coverage/', views.service_area, name='service_area'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
]
