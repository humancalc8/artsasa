from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import (
    Artwork,
    Artist,
    Category,
    Exhibition,
    ArtworkEnquiry,
)


# =========================================================
# HOME
# =========================================================

def index(request):

    featured_artworks = (
        Artwork.objects
        .filter(
            is_published=True,
            is_featured=True
        )
        .select_related(
            "artist",
            "category",
            "exhibition"
        )
        .prefetch_related(
            "images"
        )[:4]
    )

    return render(
        request,
        "index.html",
        {
            "featured_artworks": featured_artworks,
        }
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# COLLECTION
# =========================================================

def collection(request):

    artworks = (
        Artwork.objects
        .filter(
            is_published=True
        )
        .select_related(
            "artist",
            "category",
            "exhibition"
        )
        .prefetch_related(
            "images"
        )
    )

    categories = (
        Category.objects
        .filter(
            artworks__is_published=True
        )
        .distinct()
    )

    return render(
        request,
        "collection.html",
        {
            "artworks": artworks,
            "categories": categories,
        }
    )


# =========================================================
# ARTWORK / PRODUCT DETAIL
# =========================================================

class ArtworkDetailView(DetailView):

    model = Artwork

    template_name = "product_detail.html"

    context_object_name = "artwork"

    slug_field = "slug"

    slug_url_kwarg = "slug"

    def get_queryset(self):

        return (
            Artwork.objects
            .filter(
                is_published=True
            )
            .select_related(
                "artist",
                "category",
                "exhibition"
            )
            .prefetch_related(
                "images"
            )
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        artwork = self.object

        related_artworks = (
            Artwork.objects
            .filter(
                is_published=True,
                category=artwork.category
            )
            .exclude(
                pk=artwork.pk
            )
            .select_related(
                "artist",
                "category"
            )
            .prefetch_related(
                "images"
            )[:4]
        )

        context["related_artworks"] = related_artworks

        return context


# =========================================================
# ARTWORK ENQUIRY
# =========================================================

def artwork_enquiry(request, slug):

    artwork = get_object_or_404(
        Artwork,
        slug=slug,
        is_published=True
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        ArtworkEnquiry.objects.create(
            artwork=artwork,
            name=name,
            email=email,
            phone=phone,
            message=message,
        )

        return render(
            request,
            "enquiry_success.html",
            {
                "artwork": artwork,
            }
        )

    return render(
        request,
        "artwork_enquiry.html",
        {
            "artwork": artwork,
        }
    )


# =========================================================
# ARTISTS
# =========================================================

def artists(request):

    artists = Artist.objects.all()

    return render(
        request,
        "artists.html",
        {
            "artists": artists,
        }
    )


# =========================================================
# ARTIST DETAIL
# =========================================================

def artist_detail(request, slug):

    artist = get_object_or_404(
        Artist,
        slug=slug
    )

    artworks = (
        Artwork.objects
        .filter(
            artist=artist,
            is_published=True
        )
        .select_related(
            "category",
            "exhibition"
        )
        .prefetch_related(
            "images"
        )
    )

    return render(
        request,
        "artist_detail.html",
        {
            "artist": artist,
            "artworks": artworks,
        }
    )


# =========================================================
# EXHIBITIONS
# =========================================================

def exhibitions(request):

    exhibitions = Exhibition.objects.all()

    return render(
        request,
        "exhibitions.html",
        {
            "exhibitions": exhibitions,
        }
    )


# =========================================================
# EXHIBITION DETAIL
# =========================================================

def exhibition_detail(request, slug):

    exhibition = get_object_or_404(
        Exhibition,
        slug=slug
    )

    artworks = (
        Artwork.objects
        .filter(
            exhibition=exhibition,
            is_published=True
        )
        .select_related(
            "artist",
            "category"
        )
        .prefetch_related(
            "images"
        )
    )

    return render(
        request,
        "exhibition_detail.html",
        {
            "exhibition": exhibition,
            "artworks": artworks,
        }
    )