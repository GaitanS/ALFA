from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Page, Hero, Testimonial
from services.models import Service
from contact.forms import EmergencyRequestForm

@ensure_csrf_cookie
def home(request):
    """Home page view."""
    context = {
        'hero': Hero.objects.filter(is_active=True).first(),
        'services': Service.objects.filter(is_active=True).order_by('order')[:6],
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('-created_at')[:3]
    }
    return render(request, 'pages/home.html', context)

def about(request):
    """About page view."""
    context = {}
    return render(request, 'pages/about.html', context)

def emergency(request):
    """Emergency assistance page view."""
    context = {
        'form': EmergencyRequestForm()
    }
    return render(request, 'pages/emergency.html', context)

def page_detail(request, slug):
    """Generic page detail view."""
    page = get_object_or_404(Page, slug=slug, is_active=True)
    context = {
        'page': page
    }
    return render(request, f'pages/{page.template}', context)

@require_POST
def accept_cookies(request):
    """Handle cookie acceptance via AJAX."""
    try:
        # In a real application, you might want to store this in a database
        # or do additional processing
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def custom_404(request, exception):
    """Custom 404 error page."""
    return render(request, 'pages/404.html', status=404)

def custom_500(request):
    """Custom 500 error page."""
    return render(request, 'pages/500.html', status=500)

def location_view(request, location):
    """Dynamic location landing page."""
    # Map slug to display name
    locations = {
        'bristol': 'Bristol',
        'avonmouth': 'Avonmouth',
        'm4': 'M4 Motorway',
        'm5': 'M5 Motorway',
        'portbury': 'Portbury',
        'filton': 'Filton',
        'severn-beach': 'Severn Beach',
        'cribbs-causeway': 'Cribbs Causeway'
    }
    
    location_name = locations.get(location.lower())
    
    if not location_name:
        # Fallback for unknown locations or 404
        # For now, let's just capitalize it if not in map, or 404
        location_name = location.replace('-', ' ').title()

    context = {
        'location_name': location_name,
        'location_slug': location
    }
    return render(request, 'pages/location.html', context)
