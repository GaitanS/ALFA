from django.db import models

class ContactMessage(models.Model):
    URGENCY_CHOICES = [
        ('emergency', 'Emergency - Need immediate assistance'),
        ('urgent', 'Urgent - Need help soon'),
        ('general', 'General Inquiry'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='general')
    vehicle_details = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class EmergencyRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    vehicle_make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Emergency Request'
        verbose_name_plural = 'Emergency Requests'

    def __str__(self):
        return f"{self.name} - {self.location} ({self.status})"
