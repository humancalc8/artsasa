from django.urls import path

from .views import (
    index,
    about,
    collection,
    ArtworkDetailView,
    artwork_enquiry,
    artists,
    artist_detail,
    exhibitions,
    exhibition_detail,

    # Cart
    cart,
    add_to_cart,
    remove_from_cart,
    cart_count,

    # Wishlist
    wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    wishlist_count,
    live_blog_seo_analyzer,
)
from . import views
from .views import (
    index,
    about,
    collection,
    ArtworkDetailView,
    artwork_enquiry,
    artists,
    artist_detail,
    exhibitions,
    exhibition_detail,
    blog,
    blog_detail,
    # Cart
    cart,
    add_to_cart,
    remove_from_cart,
    cart_count,

    # Wishlist
    wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    wishlist_count,

    # Checkout
    checkout,
    order_success,
)
urlpatterns = [

    path("", index, name="index"),
    path("about/", about, name="about"),
    path("collection/", collection, name="collection"),
    path("artwork/<slug:slug>/", ArtworkDetailView.as_view(), name="product_detail"),
    path("artwork/<slug:slug>/enquiry/", artwork_enquiry, name="artwork_enquiry"),
    path("artists/", artists, name="artists"),
    path("artist/<slug:slug>/", artist_detail, name="artist_detail"),
  
    # CART
    path("cart/", cart, name="cart"),
   path(
    "cart/add/<int:artwork_id>/",
    views.add_to_cart,
    name="add_to_cart",
),
    path("cart/remove/", remove_from_cart, name="remove_from_cart"),
    path("cart/count/", cart_count, name="cart_count"),

    # WISHLIST
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/", views.toggle_wishlist, name="toggle_wishlist"),
    path("wishlist/add/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/", remove_from_wishlist, name="remove_from_wishlist"),
    path("wishlist/count/", wishlist_count, name="wishlist_count"),
    # CHECKOUT
path(
    "checkout/",
    checkout,
    name="checkout"
),

path(
    "order/success/<str:order_number>/",
    order_success,
    name="order_success"
),
    
    path("artists/", artists, name="artists"),
   path("blog/", blog, name="blog"),
path(
    "blog/<slug:slug>/",
    blog_detail,
    name="blog_detail"
),

    # YOUR EXISTING URLS
    # ...

    # ========================================================
    # ACCOUNT
    # ========================================================

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "verify-otp/",
        views.verify_otp_view,
        name="verify_otp"
    ),

    path(
        "resend-otp/",
        views.resend_otp_view,
        name="resend_otp"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    path(
    "privacy/",
    views.privacy,
    name="privacy"
),

path(
    "terms/",
    views.terms,
    name="terms"
),
path(
    "admin/live-blog-seo/",
    live_blog_seo_analyzer,
    name="live_blog_seo_analyzer",
),
]
