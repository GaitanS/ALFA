from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from .models import ContactMessage, EmergencyRequest

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        # Add placeholders and classes
        for field_name, field in self.fields.items():
            if field_name == 'urgency':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            if field_name == 'message':
                field.widget.attrs['rows'] = 4
                field.widget.attrs['style'] = 'height: auto'
            
            # Set placeholder to empty string for floating labels
            field.widget.attrs['placeholder'] = ' '
        
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='form-floating mb-3'),
                Div(Field('email'), css_class='form-floating mb-3'),
                Div(Field('phone'), css_class='form-floating mb-3'),
                Div(Field('urgency'), css_class='form-floating mb-3'),
                Div(Field('vehicle_details'), css_class='form-floating mb-3'),
                Div(Field('location'), css_class='form-floating mb-3'),
                Div(Field('message'), css_class='form-floating mb-3'),
            )
        )
    """Form for general contact messages."""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'urgency', 'vehicle_details', 'location', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'urgency': 'How Urgent Is Your Request?',
            'vehicle_details': 'Vehicle Details (optional)',
            'location': 'Your Location (optional)',
            'message': 'Message',
        }
        help_texts = {
            'phone': 'Enter a UK phone number',
            'vehicle_details': 'Make, model, and year of your vehicle',
            'location': 'Your current location or address',
        }

    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        # Remove any spaces or special characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Check if it's a valid UK phone number
        if not phone.startswith(('44', '0')):
            raise forms.ValidationError('Please enter a valid UK phone number.')
        
        # Format the phone number
        if phone.startswith('0'):
            phone = '44' + phone[1:]
        if not phone.startswith('+'):
            phone = '+' + phone
            
        return phone

class EmergencyRequestForm(forms.ModelForm):
    """Form for emergency assistance requests."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name', wrapper_class='mb-3', placeholder='Your Name'),
            Field('phone', wrapper_class='mb-3', placeholder='Your Phone Number'),
            Field('location', wrapper_class='mb-3', placeholder='Your Current Location'),
            Field('vehicle_make', wrapper_class='mb-3', placeholder='Vehicle Make (e.g., Ford, BMW)'),
            Field('vehicle_model', wrapper_class='mb-3', placeholder='Vehicle Model (e.g., Focus, 3 Series)'),
            Field('issue_description', wrapper_class='mb-3', placeholder='Please describe your situation', rows=3),
        )

    class Meta:
        model = EmergencyRequest
        fields = ['name', 'phone', 'location', 'vehicle_make', 'vehicle_model', 'issue_description']

    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        # Remove any spaces or special characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Check if it's a valid UK phone number
        if not phone.startswith(('44', '0')):
            raise forms.ValidationError('Please enter a valid UK phone number.')
        
        # Format the phone number
        if phone.startswith('0'):
            phone = '44' + phone[1:]
        if not phone.startswith('+'):
            phone = '+' + phone
            
        return phone

    def clean_location(self):
        """Validate location is provided."""
        location = self.cleaned_data.get('location')
        if not location:
            raise forms.ValidationError('Please provide your current location for emergency assistance.')
        return location
