
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


from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Artwork


# =========================================================
# ADD TO CART
# =========================================================

@require_POST
def add_to_cart(request, artwork_id):
    """
    Add an artwork to the session cart.

    Session structure:

        {
            "5": 1,
            "8": 2,
        }

    The keys are artwork IDs and the values are quantities.
    """

    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        is_published=True,
    )

    # -----------------------------------------------------
    # Always use the SAME session key: "cart"
    # -----------------------------------------------------

    cart = request.session.get("cart", {})

    # Session dictionary keys must be strings.
    artwork_key = str(artwork.id)

    # Existing quantity or zero.
    current_quantity = int(
        cart.get(artwork_key, 0)
    )

    # Add one.
    cart[artwork_key] = current_quantity + 1

    # Save session.
    request.session["cart"] = cart
    request.session.modified = True

    # Total number of artworks/items in cart.
    cart_count = sum(
        int(quantity)
        for quantity in cart.values()
    )

    # -----------------------------------------------------
    # AJAX RESPONSE
    # -----------------------------------------------------

    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "message": f"{artwork.title} added to cart.",
            "cart_count": cart_count,
            "count": cart_count,
            "artwork_id": artwork.id,
            "quantity": cart[artwork_key],
            "already_in_cart": current_quantity > 0,
        })

    return redirect("cart")


# =========================================================
# CART
# =========================================================

def cart(request):
    """
    Display all artworks currently stored in the session cart.

    IMPORTANT:
    This uses the exact same session key as add_to_cart()
    and cart_count():

        request.session["cart"]
    """

    # -----------------------------------------------------
    # GET CART DIRECTLY FROM SESSION
    # -----------------------------------------------------

    session_cart = request.session.get("cart", {})

    if not isinstance(session_cart, dict):
        session_cart = {}

    # -----------------------------------------------------
    # NORMALISE SESSION KEYS / QUANTITIES
    # -----------------------------------------------------

    cleaned_cart = {}

    for artwork_id, quantity in session_cart.items():

        try:
            artwork_id = str(artwork_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity > 0:
            cleaned_cart[artwork_id] = quantity

    # Keep session synchronised with cleaned data.
    if cleaned_cart != session_cart:
        request.session["cart"] = cleaned_cart
        request.session.modified = True

    session_cart = cleaned_cart

    # -----------------------------------------------------
    # NO ITEMS
    # -----------------------------------------------------

    if not session_cart:

        return render(
            request,
            "cart.html",
            {
                "cart_items": [],
                "cart_total": 0,
                "cart_count": 0,
            }
        )

    # -----------------------------------------------------
    # GET ARTWORK IDS
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
    # BUILD CART ITEMS
    # -----------------------------------------------------

    cart_items = []

    cart_total = 0

    invalid_ids = []

    total_quantity = 0

    for artwork_id in artwork_ids:

        artwork = artwork_map.get(
            str(artwork_id)
        )

        # Artwork no longer exists or isn't published.
        if not artwork:

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        # Artwork is no longer available.
        if artwork.status != "Available":

            invalid_ids.append(
                str(artwork_id)
            )

            continue

        # No price means it cannot contribute to cart total.
        # We can still show the artwork if you want "price on
        # request", so don't automatically remove it.
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

            subtotal = artwork.price * quantity

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

        cart_items.append({
            "artwork": artwork,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    # -----------------------------------------------------
    # REMOVE INVALID ITEMS FROM SESSION
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
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,

            # Total monetary value.
            "cart_total": cart_total,

            # IMPORTANT:
            # This is the number of items, including quantity.
            "cart_count": total_quantity,

            # Optional aliases useful elsewhere.
            "total_quantity": total_quantity,
            "items_count": len(cart_items),
        }
    )

# =========================================================
# CHECKOUT
# =========================================================

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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Artwork


@require_POST
def toggle_wishlist(request):
    artwork_id = request.POST.get("artwork_id")

    if not artwork_id:
        return JsonResponse(
            {
                "success": False,
                "message": "No artwork was specified."
            },
            status=400
        )

    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        is_published=True
    )

    wishlist = request.session.get("wishlist", [])

    # Convert everything to strings so session comparisons are reliable.
    wishlist = [str(item) for item in wishlist]

    artwork_id = str(artwork.id)

    if artwork_id in wishlist:
        wishlist.remove(artwork_id)
        added = False
        message = f"{artwork.title} removed from your wishlist."
    else:
        wishlist.append(artwork_id)
        added = True
        message = f"{artwork.title} added to your wishlist."

    request.session["wishlist"] = wishlist
    request.session.modified = True

    return JsonResponse(
        {
            "success": True,
            "added": added,
            "wishlist_count": len(wishlist),
            "artwork_id": artwork.id,
            "message": message,
        }
    )