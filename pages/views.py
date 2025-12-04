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


def motorway_junction_view(request, motorway, junction):
    '''Motorway junction landing page.'''
    # M4 Junctions mapping
    m4_junctions = {
        'j18': {'name': 'Junction 18', 'location': 'Bath/Tormarton', 'direction': 'towards Bristol or London'},
        'j19': {'name': 'Junction 19', 'location': 'Bristol (M32)', 'direction': 'towards Bristol city centre or London'},
        'j20': {'name': 'Junction 20', 'location': 'Almondsbury (M5)', 'direction': 'towards London or South Wales'},
        'j21': {'name': 'Junction 21', 'location': 'Pill', 'direction': 'towards Bristol or London'},
        'j22': {'name': 'Junction 22', 'location': 'Avonmouth', 'direction': 'towards Bristol or South Wales'},
    }
    
    # M5 Junctions mapping
    m5_junctions = {
        'j14': {'name': 'Junction 14', 'location': 'Thornbury/Falfield', 'direction': 'towards Birmingham or Exeter'},
        'j15': {'name': 'Junction 15', 'location': 'Almondsbury (M4)', 'direction': 'towards Birmingham or Exeter'},
        'j16': {'name': 'Junction 16', 'location': 'Aztec West', 'direction': 'towards Birmingham or Exeter'},
        'j17': {'name': 'Junction 17', 'location': 'Cribbs Causeway', 'direction': 'towards Birmingham or Exeter'},
        'j18': {'name': 'Junction 18', 'location': 'Avonmouth', 'direction': 'towards Birmingham or Exeter'},
        'j19': {'name': 'Junction 19', 'location': 'Portishead', 'direction': 'towards Birmingham or Exeter'},
    }
    
    motorway_upper = motorway.upper()
    junction_data = None
    
    if motorway_upper == 'M4':
        junction_data = m4_junctions.get(junction.lower())
    elif motorway_upper == 'M5':
        junction_data = m5_junctions.get(junction.lower())
    
    if not junction_data:
        # 404 for unknown junctions
        from django.http import Http404
        raise Http404('Junction not found')
    
    context = {
        'motorway': motorway_upper,
        'junction': junction.upper(),
        'junction_name': junction_data['name'],
        'location_name': junction_data['location'],
        'direction': junction_data['direction'],
    }
    
    return render(request, 'pages/motorway_junction.html', context)

