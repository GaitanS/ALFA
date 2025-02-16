from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('emergency/', views.emergency_request, name='emergency_request'),
    path('api/submit-contact/', views.submit_contact, name='submit_contact'),
    path('api/submit-emergency/', views.submit_emergency, name='submit_emergency'),
    path('whatsapp/', views.whatsapp_redirect, name='whatsapp_redirect'),
]
