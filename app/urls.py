from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # MAIN PAGES
    # =====================================================

    path(
        "",
        views.index,
        name="index"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "collection/",
        views.collection,
        name="collection"
    ),


    # =====================================================
    # ARTWORK / PRODUCT
    # =====================================================

    path(
        "artwork/<slug:slug>/",
        views.ArtworkDetailView.as_view(),
        name="product_detail"
    ),


    # =====================================================
    # ARTWORK ENQUIRY
    # =====================================================

    path(
        "artwork/<slug:slug>/enquire/",
        views.artwork_enquiry,
        name="artwork_enquiry"
    ),

    path(
        "artwork/<slug:slug>/",
        views.ArtworkDetailView.as_view(),
        name="artwork_detail",
    ),
]