
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

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

    # Ensure the CSRF cookie exists for AJAX cart/wishlist requests.
    csrf_token = get_token(request)

    # Current session cart.
    cart_data = request.session.get(
        "artsasa_cart",
        {}
    )

    if not isinstance(cart_data, dict):
        cart_data = {}

    # Current session wishlist.
    wishlist_data = request.session.get(
        "artsasa_wishlist",
        []
    )

    if not isinstance(wishlist_data, list):
        wishlist_data = []

    return render(
        request,
        "collection.html",
        {
            "artworks": artworks,
            "categories": categories,
            "cart_count": len(cart_data),
            "wishlist_count": len(wishlist_data),
            "cart_ids": list(cart_data.keys()),
            "wishlist_ids": wishlist_data,
            "csrf_token_value": csrf_token,
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

        # Current cart state.
        cart_data = self.request.session.get(
            "artsasa_cart",
            {}
        )

        if not isinstance(cart_data, dict):
            cart_data = {}

        # Current wishlist state.
        wishlist_data = self.request.session.get(
            "artsasa_wishlist",
            []
        )

        if not isinstance(wishlist_data, list):
            wishlist_data = []

        context["cart_count"] = len(cart_data)

        context["wishlist_count"] = len(
            wishlist_data
        )

        context["artwork_in_cart"] = str(
            artwork.pk
        ) in cart_data

        context["artwork_in_wishlist"] = str(
            artwork.pk
        ) in wishlist_data

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


# =========================================================
# CART HELPERS
# =========================================================

def get_session_cart(request):

    cart = request.session.get(
        "artsasa_cart",
        {}
    )

    if not isinstance(cart, dict):
        cart = {}

    return cart


def save_session_cart(request, cart):

    request.session["artsasa_cart"] = cart
    request.session.modified = True


def get_session_wishlist(request):

    wishlist = request.session.get(
        "artsasa_wishlist",
        []
    )

    if not isinstance(wishlist, list):
        wishlist = []

    return wishlist


def save_session_wishlist(request, wishlist):

    request.session["artsasa_wishlist"] = wishlist
    request.session.modified = True


# =========================================================
# CART COUNT
# =========================================================

def cart_count(request):

    cart = get_session_cart(request)

    # Remove malformed keys.
    clean_cart = {}

    for artwork_id in cart:

        try:
            int(artwork_id)
            clean_cart[str(artwork_id)] = 1

        except (
            TypeError,
            ValueError
        ):
            continue

    if clean_cart != cart:

        save_session_cart(
            request,
            clean_cart
        )

    return JsonResponse(
        {
            "success": True,
            "count": len(clean_cart),
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

@require_POST
def add_to_cart(request):

    artwork_id = request.POST.get(
        "artwork_id"
    )

    if not artwork_id:

        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was selected."
            },
            status=400
        )

    try:

        artwork_id = int(
            artwork_id
        )

    except (
        TypeError,
        ValueError
    ):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid artwork."
            },
            status=400
        )

    artwork = get_object_or_404(
        Artwork,
        pk=artwork_id,
        is_published=True
    )

    # -----------------------------------------------------
    # Only available artworks can be purchased.
    # -----------------------------------------------------

    if artwork.status != "Available":

        return JsonResponse(
            {
                "success": False,
                "message": (
                    f'"{artwork.title}" is '
                    f'currently {artwork.status.lower()}.'
                )
            },
            status=400
        )

    # -----------------------------------------------------
    # Artwork must have a price.
    # -----------------------------------------------------

    if artwork.price is None:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    f'"{artwork.title}" is available '
                    f'by enquiry rather than direct purchase.'
                )
            },
            status=400
        )

    cart = get_session_cart(
        request
    )

    key = str(
        artwork.pk
    )

    already_in_cart = key in cart

    # -----------------------------------------------------
    # Gallery artworks are treated as unique pieces.
    # Quantity is therefore always 1.
    # -----------------------------------------------------

    cart[key] = 1

    save_session_cart(
        request,
        cart
    )

    return JsonResponse(
        {
            "success": True,
            "already_in_cart": already_in_cart,
            "cart_count": len(cart),
            "artwork_id": artwork.pk,
            "artwork_title": artwork.title,
            "message": (
                f'"{artwork.title}" is already in your cart.'
                if already_in_cart
                else f'"{artwork.title}" has been added to your cart.'
            ),
        }
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

@require_POST
def remove_from_cart(request):

    artwork_id = request.POST.get(
        "artwork_id"
    )

    if not artwork_id:

        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was supplied."
            },
            status=400
        )

    cart = get_session_cart(
        request
    )

    key = str(
        artwork_id
    )

    removed = key in cart

    if removed:

        del cart[key]

        save_session_cart(
            request,
            cart
        )

    return JsonResponse(
        {
            "success": True,
            "removed": removed,
            "cart_count": len(cart),
            "message": (
                "Artwork removed from your cart."
                if removed
                else "Artwork was not in your cart."
            ),
        }
    )


# =========================================================
# CART PAGE
# =========================================================

def cart(request):

    session_cart = get_session_cart(
        request
    )

    artwork_ids = list(
        session_cart.keys()
    )

    artworks = (
        Artwork.objects
        .filter(
            pk__in=artwork_ids,
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

    artwork_map = {
        str(artwork.pk): artwork
        for artwork in artworks
    }

    cart_items = []

    cart_total = 0

    invalid_ids = []

    for artwork_id in artwork_ids:

        artwork = artwork_map.get(
            str(artwork_id)
        )

        if not artwork:

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        # -------------------------------------------------
        # If artwork became unavailable after being added,
        # remove it from the active shopping cart.
        # -------------------------------------------------

        if artwork.status != "Available":

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        if artwork.price is None:

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        quantity = 1

        subtotal = artwork.price

        cart_total += subtotal

        cart_items.append(
            {
                "artwork": artwork,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    # Clean invalid items.
    if invalid_ids:

        for artwork_id in invalid_ids:

            session_cart.pop(
                artwork_id,
                None
            )

        save_session_cart(
            request,
            session_cart
        )

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "cart_count": len(cart_items),
        }
    )


# =========================================================
# ADD TO WISHLIST
# =========================================================

@require_POST
def add_to_wishlist(request):

    artwork_id = request.POST.get(
        "artwork_id"
    )

    if not artwork_id:

        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was supplied."
            },
            status=400
        )

    try:

        artwork_id = int(
            artwork_id
        )

    except (
        TypeError,
        ValueError
    ):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid artwork."
            },
            status=400
        )

    artwork = get_object_or_404(
        Artwork,
        pk=artwork_id,
        is_published=True
    )

    wishlist = get_session_wishlist(
        request
    )

    key = str(
        artwork.pk
    )

    already_saved = key in wishlist

    if not already_saved:

        wishlist.append(
            key
        )

        save_session_wishlist(
            request,
            wishlist
        )

    return JsonResponse(
        {
            "success": True,
            "active": True,
            "already_saved": already_saved,
            "wishlist_count": len(wishlist),
            "message": (
                f'"{artwork.title}" is already in your wishlist.'
                if already_saved
                else f'"{artwork.title}" has been saved to your wishlist.'
            ),
        }
    )


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

@require_POST
def remove_from_wishlist(request):

    artwork_id = request.POST.get(
        "artwork_id"
    )

    if not artwork_id:

        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was supplied."
            },
            status=400
        )

    wishlist = get_session_wishlist(
        request
    )

    key = str(
        artwork_id
    )

    removed = key in wishlist

    if removed:

        wishlist.remove(
            key
        )

        save_session_wishlist(
            request,
            wishlist
        )

    return JsonResponse(
        {
            "success": True,
            "active": False,
            "wishlist_count": len(wishlist),
            "message": (
                "Artwork removed from your wishlist."
                if removed
                else "Artwork was not in your wishlist."
            ),
        }
    )


# =========================================================
# WISHLIST PAGE
# =========================================================

def wishlist(request):

    session_wishlist = get_session_wishlist(
        request
    )

    artworks = (
        Artwork.objects
        .filter(
            pk__in=session_wishlist,
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

    artwork_map = {
        str(artwork.pk): artwork
        for artwork in artworks
    }

    wishlist_items = []

    for artwork_id in session_wishlist:

        artwork = artwork_map.get(
            str(artwork_id)
        )

        if artwork:

            wishlist_items.append(
                artwork
            )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items,
            "wishlist_count": len(wishlist_items),
        }
    )

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Artwork


# =========================================================
# WISHLIST COUNT
# =========================================================

def wishlist_count(request):

    wishlist = get_session_wishlist(request)

    # Remove malformed entries
    clean_wishlist = [
        str(artwork_id)
        for artwork_id in wishlist
        if str(artwork_id).isdigit()
    ]

    if clean_wishlist != wishlist:
        save_session_wishlist(request, clean_wishlist)

    return JsonResponse(
        {
            "success": True,
            "count": len(clean_wishlist),
        }
    )