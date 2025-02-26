// Cookie Management
document.addEventListener('DOMContentLoaded', function() {
    // Function to set cookie preferences
    function setCookiePreferences(preferences) {
        localStorage.setItem('cookie_preferences', JSON.stringify(preferences));
    }

    // Function to get cookie preferences
    function getCookiePreferences() {
        const prefs = localStorage.getItem('cookie_preferences');
        return prefs ? JSON.parse(prefs) : { essential: true, analytics: false, marketing: false };
    }

    // Show cookie banner if consent not given
    if (!localStorage.getItem('cookie_preferences')) {
        document.getElementById('cookie-banner').style.display = 'block';
    }

    // Handle cookie acceptance
    document.getElementById('accept-cookies')?.addEventListener('click', function() {
        const analyticsEnabled = document.getElementById('analytics-cookies').checked;
        const marketingEnabled = document.getElementById('marketing-cookies').checked;
        setCookiePreferences({ essential: true, analytics: analyticsEnabled, marketing: marketingEnabled });
        document.getElementById('cookie-banner').style.display = 'none';

        // Send acceptance to server (example)
        fetch('/api/accept-cookies/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                accepted: true,
                analytics: analyticsEnabled,
                marketing: marketingEnabled
            })
        });
    });

    // Handle cookie decline
    document.getElementById('decline-cookies')?.addEventListener('click', function() {
        setCookiePreferences({ essential: true, analytics: false, marketing: false });
        document.getElementById('cookie-banner').style.display = 'none';
    });
});

// Form Submission Handlers
function handleFormSubmission(formId, submitUrl, successCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
        submitBtn.disabled = true;
        
        // Submit form
        fetch(submitUrl, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (successCallback) successCallback(data);
                form.reset();
            } else {
                alert(data.message || 'There was an error processing your request.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error processing your request. Please try again.');
        })
        .finally(() => {
            // Reset button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });
}

// Initialize form handlers
document.addEventListener('DOMContentLoaded', function() {
    // Contact form
    handleFormSubmission('contact-form', '/contact/api/submit-contact/', function(data) {
        alert('Thank you for your message. We will get back to you soon.');
    });
    
    // Emergency form
    handleFormSubmission('emergency-form', '/contact/api/submit-emergency/', function(data) {
        alert('Your emergency request has been submitted. We will contact you immediately.');
    });
});

// WhatsApp Redirect
function redirectToWhatsApp() {
    fetch('/contact/whatsapp/')
        .then(response => response.json())
        .then(data => {
            window.open(data.redirect_url, '_blank');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error opening WhatsApp. Please try again.');
        });
}

// Service Card Hover Effects
document.addEventListener('DOMContentLoaded', function() {
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.1)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1)';
            }
        });
    });
});

// Phone Number Formatting
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.startsWith('44')) {
        value = '+' + value;
    } else if (value.startsWith('0')) {
        value = '+44' + value.substring(1);
    }
    input.value = value;
}

// Initialize phone number formatting
document.addEventListener('DOMContentLoaded', function() {
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
});
