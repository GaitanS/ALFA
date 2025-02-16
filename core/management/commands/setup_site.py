from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import SiteSettings
from services.models import Service

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up initial data for the ALFA RECOVERY website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up initial data...')

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@alfarecovery.co.uk',
                password='admin123'  # Change this in production
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create site settings if they don't exist
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                company_name="ALFA RECOVERY Ltd",
                phone_number="+44 7722 015702",
                whatsapp_number="+44 7722 015702",
                address="Dean Rd, Avonmouth, Bristol BS11 8AT",
                operating_hours="24/7",
                meta_description="24/7 Vehicle Recovery & Roadside Assistance in the UK. Professional towing and breakdown services.",
                meta_keywords="vehicle recovery, roadside assistance, towing service, car breakdown, UK",
                google_maps_embed="""
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2485.0679863639507!2d-2.701436684280764!3d51.50661397963571!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48718e1c6cded075%3A0x8d0f0c2c8d9d7c8a!2sDean%20Rd%2C%20Avonmouth%2C%20Bristol%20BS11%208AT!5e0!3m2!1sen!2suk!4v1645000000000!5m2!1sen!2suk" 
                style="border:0; width: 100%; height: 300px;" allowfullscreen="" loading="lazy"></iframe>
                """
            )
            self.stdout.write(self.style.SUCCESS('Site settings created'))

        # Create default services if they don't exist
        default_services = [
            {
                'title': 'Vehicle Recovery',
                'description': 'Professional vehicle recovery service for cars, vans, and motorcycles. Available 24/7 across the UK.',
                'icon_class': 'fas fa-truck-pickup',
                'order': 1
            },
            {
                'title': 'Breakdown Assistance',
                'description': 'Immediate roadside assistance for breakdowns, including battery jumps, tire changes, and fuel delivery.',
                'icon_class': 'fas fa-tools',
                'order': 2
            },
            {
                'title': 'Accident Recovery',
                'description': 'Rapid response accident recovery service with careful handling and transportation of damaged vehicles.',
                'icon_class': 'fas fa-car-crash',
                'order': 3
            },
            {
                'title': 'Long Distance Recovery',
                'description': 'Nationwide vehicle transportation service for long-distance recovery needs.',
                'icon_class': 'fas fa-route',
                'order': 4
            },
            {
                'title': 'Emergency Repairs',
                'description': 'On-site emergency repairs to get you back on the road quickly and safely.',
                'icon_class': 'fas fa-wrench',
                'order': 5
            },
            {
                'title': '24/7 Emergency Service',
                'description': 'Round-the-clock emergency vehicle recovery and roadside assistance services.',
                'icon_class': 'fas fa-clock',
                'order': 6
            }
        ]

        for service_data in default_services:
            Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'icon_class': service_data['icon_class'],
                    'order': service_data['order'],
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS('Default services created'))

        self.stdout.write(self.style.SUCCESS('Initial setup completed successfully'))
        self.stdout.write('\nAdmin login details:')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        self.stdout.write('\nIMPORTANT: Please change the admin password after first login!')
