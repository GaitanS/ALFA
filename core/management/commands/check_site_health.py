from django.core.management.base import BaseCommand
import requests
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Check site health and redirects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='alfarecovery.co.uk',
            help='Domain to check (default: alfarecovery.co.uk)'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        
        # URLs to test
        test_urls = [
            f'http://{domain}/',
            f'http://www.{domain}/',
            f'https://www.{domain}/',
            f'https://{domain}/',
            f'https://{domain}/about/',
            f'https://{domain}/services/',
            f'https://{domain}/contact/',
            f'https://{domain}/sitemap.xml',
            f'https://{domain}/robots.txt',
        ]
        
        self.stdout.write(self.style.SUCCESS(f'Checking site health for {domain}...'))
        self.stdout.write('-' * 60)
        
        for url in test_urls:
            try:
                response = requests.get(url, allow_redirects=False, timeout=10)
                
                if response.status_code in [301, 302]:
                    redirect_url = response.headers.get('Location', 'No location header')
                    self.stdout.write(
                        f'{url:<40} -> {response.status_code} -> {redirect_url}'
                    )
                elif response.status_code == 200:
                    self.stdout.write(
                        self.style.SUCCESS(f'{url:<40} -> {response.status_code} OK')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'{url:<40} -> {response.status_code}')
                    )
                    
            except requests.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f'{url:<40} -> ERROR: {str(e)}')
                )
        
        self.stdout.write('-' * 60)
        self.stdout.write(self.style.SUCCESS('Site health check completed!'))
        
        # Check if canonical redirects are working
        self.stdout.write('\nCanonical redirect check:')
        try:
            # Test www to non-www redirect
            response = requests.get(f'https://www.{domain}/', allow_redirects=False, timeout=10)
            if response.status_code == 301:
                redirect_url = response.headers.get('Location', '')
                if redirect_url == f'https://{domain}/':
                    self.stdout.write(self.style.SUCCESS('✓ www to non-www redirect working'))
                else:
                    self.stdout.write(self.style.WARNING(f'✗ Unexpected redirect: {redirect_url}'))
            else:
                self.stdout.write(self.style.WARNING(f'✗ No redirect found (status: {response.status_code})'))
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'✗ Error checking redirect: {str(e)}'))