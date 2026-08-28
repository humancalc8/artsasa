from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Artist,
    Category,
    Exhibition,
    Artwork,
    ArtworkImage,
    ArtworkEnquiry,
)


# =========================================================
# ARTWORK IMAGE INLINE
# =========================================================

class ArtworkImageInline(admin.TabularInline):

    model = ArtworkImage

    extra = 3

    fields = (
        "image",
        "caption",
        "sort_order",
    )


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# =========================================================
# ARTIST
# =========================================================

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location",
        "created_at",
    )

    search_fields = (
        "name",
        "location",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# =========================================================
# EXHIBITION
# =========================================================

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "is_current",
    )

    search_fields = (
        "title",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


# =========================================================
# ARTWORK
# =========================================================

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "artist",
        "category",
        "price_display",
        "status",
        "is_featured",
        "is_published",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "is_featured",
        "is_published",
        "exhibition",
    )

    search_fields = (
        "title",
        "artist__name",
        "medium",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "status",
        "is_featured",
        "is_published",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ArtworkImageInline,
    ]

    fieldsets = (

        (
            "Artwork Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "artist",
                    "category",
                )
            }
        ),

        (
            "Artwork Images",
            {
                "fields": (
                    "image",
                )
            }
        ),

        (
            "About the Work",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            }
        ),

        (
            "Specifications",
            {
                "fields": (
                    "medium",
                    "year",
                    "dimensions",
                    "edition",
                )
            }
        ),

        (
            "Pricing & Availability",
            {
                "fields": (
                    "price",
                    "currency",
                    "status",
                )
            }
        ),

        (
            "Exhibition",
            {
                "fields": (
                    "exhibition",
                )
            }
        ),

        (
            "Website",
            {
                "fields": (
                    "is_featured",
                    "is_published",
                )
            }
        ),

        (
            "Search Engine Information",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            }
        ),

        (
            "System Information",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )


    @admin.display(
        description="Price"
    )
    def price_display(self, obj):

        if obj.price:

            return f"{obj.currency} {obj.price:,.0f}"

        return "Enquire"


# =========================================================
# ENQUIRIES
# =========================================================

@admin.register(ArtworkEnquiry)
class ArtworkEnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "artwork",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "artwork__title",
    )

    list_editable = (
        "is_read",
    )

    readonly_fields = (
        "artwork",
        "name",
        "email",
        "phone",
        "message",
        "created_at",
    )