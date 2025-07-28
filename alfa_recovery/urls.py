from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, PageSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # Cookie policy page
    path('cookie-policy/', TemplateView.as_view(
        template_name='pages/cookie_policy.html',
        extra_context={'page_title': 'Cookie Policy'}
    ), name='cookie_policy'),

    # Privacy policy page
    path('privacy-policy/', TemplateView.as_view(
        template_name='pages/privacy_policy.html',
        extra_context={'page_title': 'Privacy Policy'}
    ), name='privacy_policy'),

    # Terms and conditions page
    path('terms/', TemplateView.as_view(
        template_name='pages/terms.html',
        extra_context={'page_title': 'Terms & Conditions'}
    ), name='terms'),

    # Include app URLs
    path('services/', include('services.urls', namespace='services')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('', include('pages.urls', namespace='pages')),
]

# Add media serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'ALFA RECOVERY Administration'
admin.site.site_title = 'ALFA RECOVERY Admin Portal'
admin.site.index_title = 'Welcome to ALFA RECOVERY Admin Portal'

# Add handler404 and handler500 for custom error pages
handler404 = 'pages.views.custom_404'
handler500 = 'pages.views.custom_500'
