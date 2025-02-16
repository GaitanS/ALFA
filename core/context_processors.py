from .models import SiteSettings

def site_settings(request):
    """
    Adds site settings to the template context.
    If no settings exist, returns empty defaults.
    """
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
    except:
        settings = None

    return {
        'site_settings': settings,
        'COMPANY_COLORS': {
            'primary': '#fc2804',  # Red
            'accent': '#ffcc02',   # Yellow
        }
    }
