from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon_class')
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.order:  # If order is not set
            # Get the highest order number
            last_order = Service.objects.order_by('-order').first()
            if last_order:
                obj.order = last_order.order + 1
            else:
                obj.order = 1
        super().save_model(request, obj, form, change)
