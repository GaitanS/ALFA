from django.db import models
from ckeditor.fields import RichTextField

class Page(models.Model):
    TEMPLATE_CHOICES = [
        ('home.html', 'Home Page'),
        ('about.html', 'About Us'),
        ('services.html', 'Services'),
        ('contact.html', 'Contact'),
        ('emergency.html', 'Emergency Assistance'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    template = models.CharField(max_length=100, choices=TEMPLATE_CHOICES)
    content = RichTextField()
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Hero(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    background_image = models.ImageField(upload_to='hero/')
    cta_text = models.CharField(max_length=50, default="Request Assistance")
    cta_link = models.CharField(max_length=200, default="/emergency/")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
