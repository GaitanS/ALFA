from django.contrib import admin
from .models import SiteSettings, Service

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'phone_number', 'whatsapp_number', 'address', 'email', 'operating_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_link', 'instagram_link')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Maps', {
            'fields': ('google_maps_embed',)
        }),
    )

    def has_add_permission(self, request):
        # Check if any settings object exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)
    ordering = ('order',)
