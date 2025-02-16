from django.shortcuts import render, get_object_or_404
from .models import Service
from contact.forms import ContactForm

def service_list(request):
    """Display list of all active services."""
    services = Service.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services,
    }
    return render(request, 'services/service_list.html', context)

def service_detail(request, pk):
    """Display detailed information about a specific service."""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    
    # Get related services (excluding current service)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(
        pk=service.pk
    ).order_by('?')[:3]  # Randomly select 3 related services
    
    # Get contact form for service enquiries
    contact_form = ContactForm(initial={
        'message': f'I would like to enquire about your {service.title} service.'
    })
    
    context = {
        'service': service,
        'related_services': related_services,
        'contact_form': contact_form,
    }
    return render(request, 'services/service_detail.html', context)

def service_area(request):
    """Display information about service coverage area."""
    context = {
        'title': 'Service Area Coverage',
        'areas': [
            {
                'name': 'Bristol',
                'response_time': '30-60 minutes',
                'coverage_type': 'Primary Coverage',
            },
            {
                'name': 'South West England',
                'response_time': '1-2 hours',
                'coverage_type': 'Standard Coverage',
            },
            {
                'name': 'UK Nationwide',
                'response_time': 'Varies by location',
                'coverage_type': 'Extended Coverage',
            },
        ]
    }
    return render(request, 'services/service_area.html', context)
