from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import ContactMessage, EmergencyRequest
from .forms import ContactForm, EmergencyRequestForm

def contact(request):
    """Display contact page with contact form."""
    context = {
        'form': ContactForm(),
    }
    return render(request, 'contact/contact.html', context)

def emergency_request(request):
    """Display emergency request form."""
    context = {
        'form': EmergencyRequestForm(),
    }
    return render(request, 'contact/emergency_request.html', context)

@require_POST
def submit_contact(request):
    """Handle contact form submissions via AJAX."""
    form = ContactForm(request.POST)
    
    if form.is_valid():
        try:
            # Save the message
            message = form.save(commit=False)
            message.is_read = False
            message.save()
            
            # Send email notification
            subject = f'New Contact Message from {message.name}'
            email_context = {
                'name': message.name,
                'email': message.email,
                'phone': message.phone,
                'message': message.message,
                'urgency': message.get_urgency_display(),
            }
            
            html_message = render_to_string('contact/email/contact_notification.html', email_context)
            
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['blackmaster92@gmail.com'],  # Send to admin
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message. We will get back to you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Please correct the errors in the form.',
            'errors': form.errors
        }, status=400)

@require_POST
def submit_emergency(request):
    """Handle emergency request submissions via AJAX."""
    form = EmergencyRequestForm(request.POST)
    
    if form.is_valid():
        try:
            # Save the emergency request
            emergency = form.save(commit=False)
            emergency.status = 'pending'
            emergency.save()
            
            # Send urgent email notification
            subject = f'URGENT: Emergency Recovery Request from {emergency.name}'
            email_context = {
                'name': emergency.name,
                'phone': emergency.phone,
                'location': emergency.location,
                'vehicle_make': emergency.vehicle_make,
                'vehicle_model': emergency.vehicle_model,
                'issue_description': emergency.issue_description,
            }
            
            html_message = render_to_string('contact/email/emergency_notification.html', email_context)
            
            # Send to admin immediately
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Your emergency request has been submitted. We will contact you immediately.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Please correct the errors in the form.',
            'errors': form.errors
        }, status=400)

def whatsapp_redirect(request):
    """Handle WhatsApp redirect with pre-filled message."""
    message = "I need assistance with vehicle recovery."
    whatsapp_number = settings.WHATSAPP_NUMBER.replace('+', '')
    redirect_url = f"https://wa.me/{whatsapp_number}?text={message}"
    return JsonResponse({
        'redirect_url': redirect_url
    })
