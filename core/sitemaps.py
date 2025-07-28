from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from pages.models import Page

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['pages:home', 'pages:about', 'services:service_list', 'contact:contact']

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
