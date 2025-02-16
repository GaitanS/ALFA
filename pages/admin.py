from django.contrib import admin
from .models import Page, Hero, Testimonial

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'template', 'is_active', 'updated_at')
    list_filter = ('is_active', 'template')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'template', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'background_image')
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_link')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        # Limit to one active hero section
        if self.model.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'content')
    ordering = ('-created_at',)
