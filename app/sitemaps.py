id="q7n2vx"
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Artwork, Artist, BlogPost


class ArtsasaSitemap(Sitemap):
    protocol = "https"

    def get_domain(self, site=None):
        return "artsasa.com"


from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["index", "collection", "artists", "blog", "about", "privacy", "terms"]

    def location(self, item):
        return reverse(item)

class ArtworkSitemap(ArtsasaSitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Artwork.objects.filter(
            is_published=True
        ).order_by("pk")

    def location(self, obj):
        return reverse(
            "product_detail",
            kwargs={"slug": obj.slug},
        )

    def lastmod(self, obj):
        return obj.updated_at


class ArtistSitemap(ArtsasaSitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Artist.objects.all().order_by("pk")

    def location(self, obj):
        return reverse(
            "artist_detail",
            kwargs={"slug": obj.slug},
        )



class BlogPostSitemap(ArtsasaSitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.exclude(
            slug="new"
        ).order_by("pk")

    def location(self, obj):
        return reverse(
            "blog_detail",
            kwargs={"slug": obj.slug},
        )
