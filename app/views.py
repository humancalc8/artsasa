
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
    Order,
    OrderItem,
)
from django.db import transaction
from django.contrib import messages
from decimal import Decimal

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

    # Artists displayed on the homepage.
    # The image is optional, so artists without an uploaded
    # image will still appear with a blank circular profile.
    artists = (
        Artist.objects
        .all()
        .order_by("name")[:5]
    )

    return render(
        request,
        "index.html",
        {
            "featured_artworks": featured_artworks,
            "artists": artists,
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
        "cart",
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


from django.http import JsonResponse


from django.http import JsonResponse





# =========================================================
# REMOVE FROM CART
# =========================================================

@require_POST
def remove_from_cart(request):

    artwork_id = request.POST.get("artwork_id")

    if not artwork_id:
        if _cart_is_ajax(request):
            return JsonResponse(
                {
                    "success": False,
                    "message": "No artwork was supplied.",
                    "cart_count": _cart_count(_get_cart(request)),
                },
                status=400,
            )

        return redirect("cart")

    # -----------------------------------------------------
    # USE THE SAME CART AS ADD_TO_CART
    # -----------------------------------------------------

    cart = _get_cart(request)

    artwork_key = str(artwork_id)

    # -----------------------------------------------------
    # REMOVE ARTWORK
    # -----------------------------------------------------

    if artwork_key in cart:

        del cart[artwork_key]

        request.session["cart"] = cart
        request.session.modified = True

        removed = True

    else:

        removed = False

    # -----------------------------------------------------
    # UPDATED AUTHORITATIVE COUNT
    # -----------------------------------------------------

    cart_count = _cart_count(cart)

    # -----------------------------------------------------
    # AJAX / FETCH REQUEST
    # -----------------------------------------------------

    if _cart_is_ajax(request):

        return JsonResponse(
            {
                "success": True,
                "removed": removed,
                "cart_count": cart_count,
                "count": cart_count,
                "cart_items_count": cart_count,
                "cart_total_items": cart_count,
                "artwork_id": artwork_id,
                "message": (
                    "Artwork removed from your cart."
                    if removed
                    else "Artwork was not in your cart."
                ),
            }
        )

    # -----------------------------------------------------
    # NORMAL FORM REQUEST
    # -----------------------------------------------------

    return redirect("cart")


from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Artwork


# =========================================================
# CART HELPERS
# =========================================================

def _get_cart(request):
    """
    Return the ARTSASA cart from the session.

    The canonical session key is:

        cart

    Cart format:

        {
            "1": 1,
            "4": 1,
            "7": 1,
        }

    Artwork IDs are always stored as strings.
    """

    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    cleaned_cart = {}

    for artwork_id, quantity in cart.items():

        try:
            artwork_id = str(artwork_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity > 0:
            cleaned_cart[artwork_id] = quantity

    if cleaned_cart != cart:
        request.session["cart"] = cleaned_cart
        request.session.modified = True

    return cleaned_cart


def _cart_count(cart):
    """
    Return the total number of items in the cart.

    This counts quantities, not merely unique artwork IDs.
    """

    total = 0

    for quantity in cart.values():

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity > 0:
            total += quantity

    return total


def _cart_is_ajax(request):
    """
    Detect AJAX / fetch requests.

    Supports the standard Django-style header:

        X-Requested-With: XMLHttpRequest
    """

    return (
        request.headers.get("X-Requested-With", "").lower()
        == "xmlhttprequest"
    )


# =========================================================
# ADD TO CART
# =========================================================

@require_POST
def add_to_cart(request, artwork_id):

    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        is_published=True,
    )

    # -----------------------------------------------------
    # ARTWORK MUST BE AVAILABLE
    # -----------------------------------------------------

    if artwork.status != "Available":

        message = (
            f"{artwork.title} is not currently available."
        )

        if _cart_is_ajax(request):

            return JsonResponse(
                {
                    "success": False,
                    "message": message,
                    "cart_count": _cart_count(
                        _get_cart(request)
                    ),
                    "count": _cart_count(
                        _get_cart(request)
                    ),
                },
                status=400,
            )

        return redirect("cart")

    # -----------------------------------------------------
    # GET CURRENT CART
    # -----------------------------------------------------

    cart = _get_cart(request)

    artwork_key = str(artwork.id)

    # -----------------------------------------------------
    # CHECK WHETHER ALREADY IN CART
    # -----------------------------------------------------

    try:
        current_quantity = int(
            cart.get(artwork_key, 0)
        )
    except (TypeError, ValueError):
        current_quantity = 0

    # -----------------------------------------------------
    # UNIQUE ARTWORK
    #
    # An artwork can only appear once in the cart.
    # -----------------------------------------------------

    if current_quantity > 0:

        cart[artwork_key] = current_quantity

        already_in_cart = True

    else:

        cart[artwork_key] = 1

        already_in_cart = False

    # -----------------------------------------------------
    # SAVE SESSION
    # -----------------------------------------------------

    request.session["cart"] = cart
    request.session.modified = True

    # -----------------------------------------------------
    # AUTHORITATIVE SERVER COUNT
    # -----------------------------------------------------

    cart_count = _cart_count(cart)

    # -----------------------------------------------------
    # AJAX RESPONSE
    # -----------------------------------------------------

    if _cart_is_ajax(request):

        return JsonResponse(
            {
                "success": True,

                "message": (
                    f"{artwork.title} added to cart."
                    if not already_in_cart
                    else f"{artwork.title} is already in your cart."
                ),

                # Main authoritative count.
                "cart_count": cart_count,

                # Backwards-compatible aliases.
                "count": cart_count,
                "cart_total_items": cart_count,
                "cart_items_count": cart_count,

                "artwork_id": artwork.id,
                "quantity": cart[artwork_key],
                "already_in_cart": already_in_cart,
            }
        )

    # -----------------------------------------------------
    # NORMAL REQUEST
    # -----------------------------------------------------

    return redirect("cart")


# =========================================================
# CART COUNT
# =========================================================

def cart_count(request):
    """
    Return the current authoritative cart count.

    This endpoint is used by the navbar to refresh the
    superscript without requiring a full page reload.
    """

    cart = _get_cart(request)

    count = _cart_count(cart)

    return JsonResponse(
        {
            "success": True,

            # Primary key.
            "cart_count": count,

            # Compatibility aliases.
            "count": count,
            "cart_items_count": count,
            "cart_total_items": count,
        }
    )


# =========================================================
# CART PAGE
# =========================================================

def cart(request):
    """
    Display all artworks currently stored in the session cart.

    Uses the exact same session key:

        request.session["cart"]
    """

    # -----------------------------------------------------
    # GET / NORMALISE CART
    # -----------------------------------------------------

    session_cart = _get_cart(request)

    # -----------------------------------------------------
    # EMPTY CART
    # -----------------------------------------------------

    if not session_cart:

        return render(
            request,
            "cart.html",
            {
                "cart_items": [],
                "cart_total": 0,
                "cart_count": 0,
                "total_quantity": 0,
                "items_count": 0,
            },
        )

    # -----------------------------------------------------
    # ARTWORK IDS
    # -----------------------------------------------------

    artwork_ids = list(
        session_cart.keys()
    )

    # -----------------------------------------------------
    # FETCH ARTWORKS
    # -----------------------------------------------------

    artworks = (
        Artwork.objects
        .filter(
            pk__in=artwork_ids,
            is_published=True,
        )
        .select_related(
            "artist",
            "category",
            "exhibition",
        )
        .prefetch_related(
            "images",
        )
    )

    artwork_map = {
        str(artwork.pk): artwork
        for artwork in artworks
    }

    # -----------------------------------------------------
    # BUILD CART
    # -----------------------------------------------------

    cart_items = []

    cart_total = 0

    invalid_ids = []

    total_quantity = 0

    for artwork_id in artwork_ids:

        artwork = artwork_map.get(
            str(artwork_id)
        )

        # -------------------------------------------------
        # ARTWORK NO LONGER EXISTS
        # -------------------------------------------------

        if not artwork:

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        # -------------------------------------------------
        # ARTWORK NO LONGER AVAILABLE
        # -------------------------------------------------

        if artwork.status != "Available":

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        # -------------------------------------------------
        # QUANTITY
        # -------------------------------------------------

        quantity = session_cart.get(
            str(artwork_id),
            1,
        )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        # -------------------------------------------------
        # SUBTOTAL
        # -------------------------------------------------

        if artwork.price is not None:

            subtotal = (
                artwork.price * quantity
            )

            cart_total += subtotal

        else:

            subtotal = None

        # -------------------------------------------------
        # TOTAL QUANTITY
        # -------------------------------------------------

        total_quantity += quantity

        # -------------------------------------------------
        # CART ITEM
        # -------------------------------------------------

        cart_items.append(
            {
                "artwork": artwork,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    # -----------------------------------------------------
    # REMOVE INVALID ITEMS
    # -----------------------------------------------------

    if invalid_ids:

        for artwork_id in invalid_ids:

            session_cart.pop(
                str(artwork_id),
                None,
            )

        request.session["cart"] = session_cart
        request.session.modified = True

    # -----------------------------------------------------
    # FINAL SERVER COUNT
    # -----------------------------------------------------

    total_quantity = _cart_count(
        session_cart
    )

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,

            "cart_total": cart_total,

            # Navbar / template count.
            "cart_count": total_quantity,

            # Useful aliases.
            "total_quantity": total_quantity,
            "items_count": len(cart_items),
        },
    )

def checkout(request):

    session_cart = request.session.get(
        "cart",
        {}
    )

    if not isinstance(session_cart, dict):
        session_cart = {}

    # -----------------------------------------------------
    # EMPTY CART
    # -----------------------------------------------------

    if not session_cart:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart")

    # -----------------------------------------------------
    # GET ARTWORKS
    # -----------------------------------------------------

    artwork_ids = list(
        session_cart.keys()
    )

    artworks = (
        Artwork.objects
        .filter(
            pk__in=artwork_ids,
            is_published=True,
        )
        .select_related(
            "artist",
            "category",
            "exhibition",
        )
        .prefetch_related(
            "images",
        )
    )

    artwork_map = {
        str(artwork.pk): artwork
        for artwork in artworks
    }

    checkout_items = []

    total = Decimal("0.00")

    # -----------------------------------------------------
    # BUILD CHECKOUT
    # -----------------------------------------------------

    for artwork_id, quantity in session_cart.items():

        artwork = artwork_map.get(
            str(artwork_id)
        )

        if not artwork:
            continue

        # Artwork must still be available.
        if artwork.status != "Available":
            messages.error(
                request,
                f'"{artwork.title}" is no longer available.'
            )

            return redirect("cart")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        # Unique artworks should only be ordered once.
        if quantity < 1:
            quantity = 1

        if artwork.price is not None:

            subtotal = (
                artwork.price *
                quantity
            )

            total += subtotal

        else:

            subtotal = None

        checkout_items.append({
            "artwork": artwork,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    # -----------------------------------------------------
    # NOTHING VALID
    # -----------------------------------------------------

    if not checkout_items:

        messages.warning(
            request,
            "There are no available artworks in your cart."
        )

        return redirect("cart")

    # =====================================================
    # POST — CREATE ORDER
    # =====================================================

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

        country = request.POST.get(
            "country",
            "Kenya"
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        errors = []

        if not name:
            errors.append(
                "Please enter your full name."
            )

        if not email:
            errors.append(
                "Please enter your email address."
            )

        if not phone:
            errors.append(
                "Please enter your phone number."
            )

        if errors:

            for error in errors:
                messages.error(
                    request,
                    error
                )

        else:

            # ---------------------------------------------
            # RE-CHECK AVAILABILITY INSIDE TRANSACTION
            # ---------------------------------------------

            try:

                with transaction.atomic():

                    locked_artworks = (
                        Artwork.objects
                        .select_for_update()
                        .filter(
                            pk__in=artwork_ids,
                            is_published=True,
                        )
                    )

                    locked_map = {
                        str(artwork.pk): artwork
                        for artwork in locked_artworks
                    }

                    final_total = Decimal("0.00")

                    final_items = []

                    for artwork_id, quantity in session_cart.items():

                        artwork = locked_map.get(
                            str(artwork_id)
                        )

                        if not artwork:

                            raise ValueError(
                                "One of the artworks in your cart "
                                "is no longer available."
                            )

                        if artwork.status != "Available":

                            raise ValueError(
                                f'"{artwork.title}" is no longer available.'
                            )

                        try:
                            quantity = int(quantity)
                        except (
                            TypeError,
                            ValueError
                        ):
                            quantity = 1

                        if quantity < 1:
                            quantity = 1

                        if artwork.price is not None:

                            subtotal = (
                                artwork.price *
                                quantity
                            )

                            final_total += subtotal

                        else:

                            subtotal = None

                        final_items.append({
                            "artwork": artwork,
                            "quantity": quantity,
                            "subtotal": subtotal,
                        })

                    # -----------------------------------------
                    # CREATE ORDER
                    # -----------------------------------------

                    order = Order.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        country=country,
                        city=city,
                        address=address,
                        message=message,
                        total=(
                            final_total
                            if final_total > 0
                            else None
                        ),
                        currency="KES",
                        status="Pending",
                    )

                    # -----------------------------------------
                    # CREATE ORDER ITEMS
                    # -----------------------------------------

                    for item in final_items:

                        artwork = item["artwork"]

                        OrderItem.objects.create(
                            order=order,
                            artwork=artwork,
                            title=artwork.title,
                            artist_name=(
                                artwork.artist.name
                                if artwork.artist
                                else ""
                            ),
                            quantity=item["quantity"],
                            price=artwork.price,
                            currency=artwork.currency,
                            subtotal=item["subtotal"],
                        )

                    # -----------------------------------------
                    # CLEAR CART
                    # -----------------------------------------

                    request.session["cart"] = {}

                    request.session.modified = True

                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                return redirect(
                    "order_success",
                    order_number=order.order_number
                )

            except ValueError as exc:

                messages.error(
                    request,
                    str(exc)
                )

                return redirect("cart")

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "checkout.html",
        {
            "checkout_items": checkout_items,
            "checkout_total": total,
        }
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

def order_success(request, order_number):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items"
        ),
        order_number=order_number,
    )

    return render(
        request,
        "order_success.html",
        {
            "order": order,
        }
    )
# =========================================================
# CART COUNT
# =========================================================

def cart_count(request):
    """
    Return the total quantity in the session cart.

    Uses the exact same "cart" session key as cart()
    and add_to_cart().
    """

    cart = request.session.get(
        "cart",
        {},
    )

    if not isinstance(cart, dict):
        cart = {}

    count = 0

    for quantity in cart.values():

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity > 0:
            count += quantity

    return JsonResponse({
        "success": True,
        "count": count,
        "cart_count": count,
    })
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Artwork


# =========================================================
# WISHLIST HELPERS
# =========================================================

def get_session_wishlist(request):
    """
    Get the ARTSASA wishlist from the current session.

    The entire website uses ONE session key:

        artsasa_wishlist

    Wishlist IDs are stored as strings.
    """

    wishlist = request.session.get(
        "artsasa_wishlist",
        []
    )

    if not isinstance(wishlist, list):
        wishlist = []

    # Normalize IDs to strings and remove duplicates.
    wishlist = list(
        dict.fromkeys(
            str(item)
            for item in wishlist
            if str(item).isdigit()
        )
    )

    return wishlist


def save_session_wishlist(request, wishlist):
    """
    Save the ARTSASA wishlist to the session.
    """

    cleaned = list(
        dict.fromkeys(
            str(item)
            for item in wishlist
            if str(item).isdigit()
        )
    )

    request.session["artsasa_wishlist"] = cleaned
    request.session.modified = True


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

    artwork_key = str(
        artwork.pk
    )

    already_saved = (
        artwork_key in wishlist
    )

    if not already_saved:

        wishlist.append(
            artwork_key
        )

        save_session_wishlist(
            request,
            wishlist
        )

    wishlist_count = len(
        wishlist
    )

    return JsonResponse(
        {
            "success": True,
            "active": True,
            "added": not already_saved,
            "already_saved": already_saved,
            "artwork_id": artwork.pk,
            "wishlist_count": wishlist_count,
            "count": wishlist_count,
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

    artwork_key = str(
        artwork_id
    )

    removed = (
        artwork_key in wishlist
    )

    if removed:

        wishlist.remove(
            artwork_key
        )

        save_session_wishlist(
            request,
            wishlist
        )

    wishlist_count = len(
        wishlist
    )

    return JsonResponse(
        {
            "success": True,
            "active": False,
            "added": False,
            "removed": removed,
            "artwork_id": artwork_id,
            "wishlist_count": wishlist_count,
            "count": wishlist_count,
            "message": (
                "Artwork removed from your wishlist."
                if removed
                else "Artwork was not in your wishlist."
            ),
        }
    )


# =========================================================
# TOGGLE WISHLIST
# =========================================================

@require_POST
def toggle_wishlist(request):

    artwork_id = request.POST.get(
        "artwork_id"
    )

    if not artwork_id:
        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was specified."
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

    artwork_key = str(
        artwork.pk
    )

    if artwork_key in wishlist:

        wishlist.remove(
            artwork_key
        )

        added = False
        active = False

        message = (
            f'"{artwork.title}" removed from your wishlist.'
        )

    else:

        wishlist.append(
            artwork_key
        )

        added = True
        active = True

        message = (
            f'"{artwork.title}" added to your wishlist.'
        )

    save_session_wishlist(
        request,
        wishlist
    )

    wishlist_count = len(
        wishlist
    )

    return JsonResponse(
        {
            "success": True,
            "added": added,
            "active": active,
            "artwork_id": artwork.pk,
            "wishlist_count": wishlist_count,
            "count": wishlist_count,
            "message": message,
        }
    )


# =========================================================
# WISHLIST COUNT
# =========================================================

def wishlist_count(request):

    wishlist = get_session_wishlist(
        request
    )

    # Remove artwork IDs that no longer exist.
    valid_ids = set(
        str(pk)
        for pk in Artwork.objects.filter(
            pk__in=wishlist,
            is_published=True
        ).values_list(
            "pk",
            flat=True
        )
    )

    cleaned_wishlist = [
        artwork_id
        for artwork_id in wishlist
        if artwork_id in valid_ids
    ]

    if cleaned_wishlist != wishlist:

        save_session_wishlist(
            request,
            cleaned_wishlist
        )

    count = len(
        cleaned_wishlist
    )

    return JsonResponse(
        {
            "success": True,
            "count": count,
            "wishlist_count": count,
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

    # Clean the session if an artwork
    # was deleted/unpublished.
    valid_wishlist = [
        str(artwork.pk)
        for artwork in wishlist_items
    ]

    if valid_wishlist != session_wishlist:

        save_session_wishlist(
            request,
            valid_wishlist
        )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items,
            "wishlist_count": len(
                wishlist_items
            ),
        }
    )
from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import BlogPost


from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from datetime import timedelta

# ============================================================
# BLOG
# ============================================================

def blog(request):
    """
    Main ARTSASA Journal / Blog page.
    Only published articles are visible publicly.
    """

    posts = (
        BlogPost.objects
        .filter(published=True)
        .select_related("category")
        .order_by(
            "-published_at",
            "-created_at"
        )
    )

    featured_post = (
        posts
        .filter(featured=True)
        .first()
    )

    paginator = Paginator(
        posts,
        9
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "featured_post": featured_post,
    }

    return render(
        request,
        "blog.html",
        context
    )


# ============================================================
# BLOG ARTICLE
# ============================================================

def blog_detail(request, slug):
    """
    Individual published blog article.
    """

    post = get_object_or_404(
        BlogPost.objects.select_related(
            "category"
        ),
        slug=slug,
        published=True
    )

    return render(
        request,
        "blog_detail.html",
        {
            "post": post,
        }
    )
# =========================================================
# LIVE BLOG SEO ANALYZER
# =========================================================

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required

from .seo_analyzer import analyze_blog


@staff_member_required
@require_POST
def live_blog_seo_analyzer(request):
    """
    Runs the ARTSASA blog SEO analyzer against the values
    currently entered in the Django admin form.

    Nothing is saved to the database.
    """

    title = request.POST.get("title", "")
    slug = request.POST.get("slug", "")
    excerpt = request.POST.get("excerpt", "")
    content = request.POST.get("content", "")
    focus_keyword = request.POST.get("focus_keyword", "")
    seo_title = request.POST.get("meta_title", "")
    meta_description = request.POST.get("meta_description", "")
    image_alt = request.POST.get("image_alt", "")

    analysis = analyze_blog(
        title=title,
        slug=slug,
        excerpt=excerpt,
        content=content,
        focus_keyword=focus_keyword,
        seo_title=seo_title,
        meta_description=meta_description,
        featured_image=None,
        image_alt=image_alt,
    )

    return JsonResponse(analysis)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import RegisterForm, OTPVerificationForm, LoginForm
from .models import EmailVerification
from .utils import send_verification_otp
# ============================================================
# ACCOUNT REGISTRATION
# ============================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            # Create inactive user until email is verified
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            user.is_active = False
            user.save(update_fields=["is_active"])

            verification = EmailVerification.objects.create(
            user=user,
)

            send_verification_otp(
                user,
                verification,
)

            # Remember user while verifying
            request.session["pending_verification_user_id"] = user.id

            messages.success(
                request,
                "Your account has been created. "
                "We sent a verification code to your email."
            )

            return redirect("verify_otp")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        }
    )


# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp_view(request):

    user_id = request.session.get(
        "pending_verification_user_id"
    )

    if not user_id:
        messages.error(
            request,
            "Your verification session has expired. Please register again."
        )
        return redirect("register")

    try:
        user = User.objects.get(
            id=user_id
        )

        verification = EmailVerification.objects.get(
            user=user
        )

    except (
        User.DoesNotExist,
        EmailVerification.DoesNotExist
    ):
        messages.error(
            request,
            "Verification information could not be found."
        )
        return redirect("register")

    if verification.is_verified:
        request.session.pop(
            "pending_verification_user_id",
            None
        )

        return redirect("login")

    if request.method == "POST":

        form = OTPVerificationForm(request.POST)

        if form.is_valid():

            otp = form.cleaned_data["otp"]

            # Maximum 5 attempts
            if verification.attempts >= 5:

                messages.error(
                    request,
                    "Too many incorrect attempts. Please request a new code."
                )

                return redirect("verify_otp")

            if verification.is_expired:

                messages.error(
                    request,
                    "This verification code has expired. "
                    "Please request a new code."
                )

                return redirect("verify_otp")

            if not verification.check_otp(otp):

                verification.attempts += 1

                verification.save(
                    update_fields=["attempts"]
                )

                remaining = max(
                    0,
                    5 - verification.attempts
                )

                messages.error(
                    request,
                    f"Incorrect verification code. "
                    f"{remaining} attempts remaining."
                )

                return redirect("verify_otp")

            # ==================================================
            # SUCCESSFUL VERIFICATION
            # ==================================================

            user.is_active = True

            user.save(
                update_fields=["is_active"]
            )

            verification.verified_at = timezone.now()

            verification.save(
                update_fields=["verified_at"]
            )

            request.session.pop(
                "pending_verification_user_id",
                None
            )

            # Automatically log user in
            login(
                request,
                user
            )

            messages.success(
                request,
                "Your email has been verified. Welcome to ARTSASA!"
            )

            return redirect("index")

    else:
        form = OTPVerificationForm()

    return render(
        request,
        "accounts/verify_otp.html",
        {
            "form": form,
            "user": user,
            "verification": verification,
        }
    )


# ============================================================
# RESEND OTP
# ============================================================

def resend_otp_view(request):

    user_id = request.session.get(
        "pending_verification_user_id"
    )

    if not user_id:
        messages.error(
            request,
            "Your verification session has expired."
        )
        return redirect("register")

    try:
        user = User.objects.get(
            id=user_id
        )

        verification = EmailVerification.objects.get(
            user=user
        )

    except (
        User.DoesNotExist,
        EmailVerification.DoesNotExist
    ):
        messages.error(
            request,
            "Verification information could not be found."
        )
        return redirect("register")

    # Prevent rapid OTP spam
    if verification.last_sent_at:

        seconds_since_last_send = (
            timezone.now() - verification.last_sent_at
        ).total_seconds()

        if seconds_since_last_send < 60:

            remaining = int(
                60 - seconds_since_last_send
            )

            messages.warning(
                request,
                f"Please wait {remaining} seconds before requesting another code."
            )

            return redirect("verify_otp")

    send_verification_otp(
        user,
        verification
    )

    messages.success(
        request,
        "A new verification code has been sent to your email."
    )

    return redirect("verify_otp")


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(
                    email__iexact=email
                )
            except User.DoesNotExist:
                user = None

            # Account exists but email hasn't been verified
            if user and not user.is_active:

                verification = getattr(
                    user,
                    "email_verification",
                    None
                )

                if verification and not verification.is_verified:

                    request.session[
                        "pending_verification_user_id"
                    ] = user.id

                    messages.warning(
                        request,
                        "Please verify your email before logging in."
                    )

                    return redirect("verify_otp")

            authenticated_user = authenticate(
                request,
                username=email,
                password=password
            )

            if authenticated_user is not None:

                login(
                    request,
                    authenticated_user
                )

                messages.success(
                    request,
                    f"Welcome back, {authenticated_user.first_name}!"
                )

                next_url = request.GET.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("index")

            messages.error(
                request,
                "Invalid email or password."
            )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@require_POST
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been signed out."
    )

    return redirect("index")

# =========================================================
# PRIVACY POLICY
# =========================================================

def privacy(request):
    return render(
        request,
        "privacy.html"
    )


# =========================================================
# TERMS & CONDITIONS
# =========================================================

def terms(request):
    return render(
        request,
        "terms.html"
    )