from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fas fa-truck')"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title
