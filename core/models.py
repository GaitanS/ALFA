from django.db import models
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    company_name = models.CharField(max_length=100, default="ALFA RECOVERY Ltd")
    phone_number = models.CharField(max_length=20, default="+44 7722 015702")
    whatsapp_number = models.CharField(max_length=20, default="+44 7722 015702")
    address = models.CharField(max_length=255, default="Dean Rd, Avonmouth, Bristol BS11 8AT")
    email = models.EmailField(max_length=254, blank=True)
    operating_hours = models.CharField(max_length=100, default="24/7")
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    meta_description = models.TextField(
        max_length=160,
        default="Expert HGV and commercial vehicle recovery in Bristol. 24/7 emergency roadside assistance for trucks, vans, and fleets."
    )
    meta_keywords = models.CharField(
        max_length=255,
        default="HGV recovery Bristol, commercial recovery Bristol, vehicle recovery, roadside assistance, towing service, car breakdown, UK"
    )
    google_maps_embed = models.TextField(
        blank=True,
        help_text="Paste your Google Maps embed code here"
    )

    def clean(self):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Only one site settings instance can exist.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.company_name

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fas fa-truck')"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
