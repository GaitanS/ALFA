from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Emergency assistance page
    path('emergency/', views.emergency, name='emergency'),
    
    # Location pages
    path('recovery/<slug:location>/', views.location_view, name='location'),
    
    # Motorway junction pages
    path('recovery/<str:motorway>/<str:junction>/', views.motorway_junction_view, name='motorway_junction'),
    
    # Dynamic page handler
    path('<slug:slug>/', views.page_detail, name='page_detail'),
    
    # AJAX endpoints
    path('api/accept-cookies/', views.accept_cookies, name='accept_cookies'),
]
