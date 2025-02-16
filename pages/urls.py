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
    
    # Dynamic page handler
    path('<slug:slug>/', views.page_detail, name='page_detail'),
    
    # AJAX endpoints
    path('api/accept-cookies/', views.accept_cookies, name='accept_cookies'),
]
