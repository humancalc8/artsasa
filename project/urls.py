from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.decorators.http import require_GET

from app.sitemaps import (
    ArtistSitemap,
    ArtworkSitemap,
    BlogPostSitemap,
    StaticViewSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "artworks": ArtworkSitemap,
    "artists": ArtistSitemap,
    "blog": BlogPostSitemap,
}


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /controls/",
        "Disallow: /ckeditor5/",
        "Disallow: /cart/",
        "Disallow: /wishlist/",
        "",
        "Sitemap: https://artsasa.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    # SEO files first, so nothing in app.urls can swallow them
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django_sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),

    path("controls/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )