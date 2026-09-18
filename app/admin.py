from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Artist, Exhibition
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
from .models import (
    Order,
    OrderItem,
)
# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "artwork",
        "title",
        "artist_name",
        "quantity",
        "price",
        "currency",
        "subtotal",
        "created_at",
    )

    can_delete = False


# =========================================================
# ORDER ADMIN
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "name",
        "email",
        "phone",
        "total_display",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "order_number",
        "name",
        "email",
        "phone",
    )

    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
        "total",
        "currency",
    )

    inlines = [
        OrderItemInline
    ]

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Order",
            {
                "fields": (
                    "order_number",
                    "status",
                )
            }
        ),

        (
            "Customer",
            {
                "fields": (
                    "name",
                    "email",
                    "phone",
                    "country",
                    "city",
                    "address",
                    "message",
                )
            }
        ),

        (
            "Order Total",
            {
                "fields": (
                    "total",
                    "currency",
                )
            }
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )

    def total_display(self, obj):

        if obj.total is None:
            return "Price on request"

        return f"{obj.currency} {obj.total:,.2f}"

    total_display.short_description = "Total"

from django.contrib import admin
from .models import EmailVerification


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "email",
        "verification_status",
        "expires_at",
        "attempts",
        "verified_at",
        "created_at",
    )

    list_filter = (
        "verified_at",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "otp_hash",
        "created_at",
        "last_sent_at",
        "verified_at",
    )

    ordering = (
        "-created_at",
    )

    def email(self, obj):
        return obj.user.email

    email.short_description = "Email"

    def verification_status(self, obj):

        if obj.is_verified:
            return "Verified"

        if obj.is_expired:
            return "Expired"

        return "Pending"

    verification_status.short_description = "Status"


from django.contrib import admin

from .models import (
    BlogCategory,
    BlogPost,
)


# ============================================================
# BLOG CATEGORY
# ============================================================

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }


# ============================================================
# BLOG POST
# ============================================================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "author",
        "published",
        "featured",
        "published_at",
        "created_at",
    )

    list_filter = (
        "published",
        "featured",
        "category",
        "published_at",
    )

    search_fields = (
        "title",
        "excerpt",
        "content",
        "author",
        "meta_title",
        "meta_description",
    )

    prepopulated_fields = {
        "slug": (
            "title",
        )
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Article",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "author",
                    "excerpt",
                    "content",
                    "featured_image",
                )
            }
        ),

        (
            "Publishing",
            {
                "fields": (
                    "published",
                    "featured",
                    "published_at",
                )
            }
        ),

        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            }
        ),

        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )
