from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from app.sitemaps import (
StaticViewSitemap,
ArtworkSitemap,
ArtistSitemap,

BlogPostSitemap,
)

sitemaps = {
"static": StaticViewSitemap,
"artworks": ArtworkSitemap,
"artists": ArtistSitemap,

"blog": BlogPostSitemap,
}

urlpatterns = [
path("controls/", admin.site.urls),
path("", include("app.urls")),
path("ckeditor5/", include("django_ckeditor_5.urls")),

path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
    name="django_sitemap",
),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )