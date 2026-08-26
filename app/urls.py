from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),

    path(
        "collection/",
        views.collection_view,
        name="collection"
    ),

    path(
        "about/",
        views.about_view,
        name="about"
    ),
]