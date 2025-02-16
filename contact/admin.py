from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, EmergencyRequest

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'urgency', 'created_at', 'is_read')
    list_filter = ('urgency', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('urgency', 'vehicle_details', 'location', 'message')
        }),
        ('Admin', {
            'fields': ('is_read', 'notes', 'created_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.is_read = False
        super().save_model(request, obj, form, change)

@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'location_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'location', 'vehicle_make', 'vehicle_model')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'phone')
        }),
        ('Location & Vehicle', {
            'fields': ('location', 'vehicle_make', 'vehicle_model')
        }),
        ('Request Details', {
            'fields': ('issue_description', 'status')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def location_display(self, obj):
        """Display location with a clickable Google Maps link"""
        maps_url = f"https://www.google.com/maps/search/?api=1&query={obj.location.replace(' ', '+')}"
        return format_html('<a href="{}" target="_blank">{}</a>', maps_url, obj.location)
    location_display.short_description = 'Location'

    def save_model(self, request, obj, form, change):
        if not change and not obj.status:  # If this is a new object
            obj.status = 'pending'
        super().save_model(request, obj, form, change)
