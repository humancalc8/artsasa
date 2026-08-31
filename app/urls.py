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
)

urlpatterns = [

    path("", index, name="index"),
    path("about/", about, name="about"),
    path("collection/", collection, name="collection"),
    path("artwork/<slug:slug>/", ArtworkDetailView.as_view(), name="product_detail"),
    path("artwork/<slug:slug>/enquiry/", artwork_enquiry, name="artwork_enquiry"),
    path("artists/", artists, name="artists"),
    path("artist/<slug:slug>/", artist_detail, name="artist_detail"),
    path("exhibitions/", exhibitions, name="exhibitions"),
    path("exhibition/<slug:slug>/", exhibition_detail, name="exhibition_detail"),

    # CART
    path("cart/", cart, name="cart"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/remove/", remove_from_cart, name="remove_from_cart"),
    path("cart/count/", cart_count, name="cart_count"),

    # WISHLIST
    path("wishlist/", wishlist, name="wishlist"),
    path("wishlist/add/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/", remove_from_wishlist, name="remove_from_wishlist"),
    path("wishlist/count/", wishlist_count, name="wishlist_count"),
]