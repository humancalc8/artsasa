from django.contrib import admin
from .seo_analyzer import analyze_blog
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

from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    change_form_template = "admin/blog/blogpost/change_form.html"

    # =========================================================
    # LIST
    # =========================================================

    list_display = (
        "title",
        "category",
        "author",
        "seo_score_display",
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
        "focus_keyword",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "seo_analysis",
    )

    # =========================================================
    # FIELDSETS
    # =========================================================

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
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "focus_keyword",
                    "meta_title",
                    "meta_description",
                    "image_alt",
                    "seo_analysis",
                ),
                "description": (
                    "Search-engine optimization settings and "
                    "the automatic ARTSASA SEO analysis."
                ),
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

    # =========================================================
    # SEO SCORE IN ADMIN LIST
    # =========================================================

    @admin.display(
        description="SEO",
        ordering=False,
    )
    def seo_score_display(self, obj):

        try:

            result = self._run_seo_analysis(
                obj
            )

            score = result["score"]

            if score >= 90:
                return f"{score}/100 — Excellent"

            if score >= 80:
                return f"{score}/100 — Very good"

            if score >= 70:
                return f"{score}/100 — Good"

            if score >= 50:
                return f"{score}/100 — Needs work"

            return f"{score}/100 — Poor"

        except Exception:

            return "—"

    # =========================================================
    # SEO ANALYSIS
    # =========================================================

    @admin.display(
        description="SEO analysis"
    )
    def seo_analysis(self, obj):

        result = self._run_seo_analysis(
            obj
        )

        score = result["score"]
        rating = result["rating"]

        checks = result["checks"]
        recommendations = result["recommendations"]
        metrics = result["metrics"]

        # -----------------------------------------------------
        # Score colour
        # -----------------------------------------------------

        if score >= 90:
            score_class = "excellent"

        elif score >= 80:
            score_class = "very-good"

        elif score >= 70:
            score_class = "good"

        elif score >= 50:
            score_class = "needs-work"

        else:
            score_class = "poor"

        # -----------------------------------------------------
        # Checks
        # -----------------------------------------------------

        checks_html = ""

        for check in checks:

            if check["passed"]:

                icon = "✓"
                state = "pass"

            else:

                icon = "!"
                state = "warning"

            checks_html += f"""
                <div class="artsasa-seo-check {state}">
                    <div class="artsasa-seo-check-icon">
                        {icon}
                    </div>

                    <div class="artsasa-seo-check-content">

                        <div class="artsasa-seo-check-title">
                            {check["label"]}
                        </div>

                        <div class="artsasa-seo-check-message">
                            {check["message"]}
                        </div>

                    </div>

                    <div class="artsasa-seo-points">
                        {check["points"]}/{check["max_points"]}
                    </div>
                </div>
            """

        # -----------------------------------------------------
        # Recommendations
        # -----------------------------------------------------

        recommendations_html = ""

        if recommendations:

            for item in recommendations:

                recommendations_html += f"""
                    <li>
                        <strong>
                            {item["label"]}
                        </strong>

                        <span>
                            {item["text"]}
                        </span>
                    </li>
                """

        else:

            recommendations_html = """
                <li class="artsasa-seo-all-good">
                    <strong>All checks passed.</strong>
                    <span>
                        No immediate SEO recommendations.
                    </span>
                </li>
            """

        # -----------------------------------------------------
        # Return HTML
        # -----------------------------------------------------

        return format_html(
            """
            <div class="artsasa-seo-panel">

                <div class="artsasa-seo-header">

                    <div>

                        <div class="artsasa-seo-eyebrow">
                            ARTSASA SEO ANALYSIS
                        </div>

                        <div class="artsasa-seo-heading">
                            Search visibility
                        </div>

                    </div>

                    <div class="artsasa-seo-score {score_class}">

                        <strong>
                            {score}
                        </strong>

                        <span>
                            / 100
                        </span>

                    </div>

                </div>


                <div class="artsasa-seo-rating">
                    {rating}
                </div>


                <div class="artsasa-seo-progress">

                    <div
                        class="artsasa-seo-progress-bar"
                        style="width: {score}%"
                    ></div>

                </div>


                <div class="artsasa-seo-metrics">

                    <div>
                        <strong>
                            {word_count:,}
                        </strong>

                        <span>
                            Words
                        </span>
                    </div>

                    <div>
                        <strong>
                            {heading_count}
                        </strong>

                        <span>
                            Headings
                        </span>
                    </div>

                    <div>
                        <strong>
                            {link_count}
                        </strong>

                        <span>
                            Links
                        </span>
                    </div>

                    <div>
                        <strong>
                            {image_count}
                        </strong>

                        <span>
                            Images
                        </span>
                    </div>

                </div>


                <div class="artsasa-seo-section">

                    <div class="artsasa-seo-section-title">
                        SEO checks
                    </div>

                    <div class="artsasa-seo-checks">
                        {checks_html}
                    </div>

                </div>


                <div class="artsasa-seo-section">

                    <div class="artsasa-seo-section-title">
                        Recommendations
                    </div>

                    <ul class="artsasa-seo-recommendations">
                        {recommendations_html}
                    </ul>

                </div>

            </div>


            <style>

                .artsasa-seo-panel {{
                    margin-top: 12px;
                    max-width: 980px;
                    background: #f8f6f1;
                    border: 1px solid #ddd7cc;
                    border-radius: 14px;
                    padding: 28px;
                    color: #211e1b;
                    box-sizing: border-box;
                }}

                .artsasa-seo-header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 24px;
                }}

                .artsasa-seo-eyebrow {{
                    font-size: 10px;
                    letter-spacing: .18em;
                    text-transform: uppercase;
                    color: #83807a;
                    margin-bottom: 7px;
                    font-weight: 600;
                }}

                .artsasa-seo-heading {{
                    font-family: Georgia, serif;
                    font-size: 25px;
                    line-height: 1.1;
                }}

                .artsasa-seo-score {{
                    display: flex;
                    align-items: baseline;
                    white-space: nowrap;
                }}

                .artsasa-seo-score strong {{
                    font-size: 44px;
                    line-height: 1;
                }}

                .artsasa-seo-score span {{
                    font-size: 14px;
                    color: #83807a;
                    margin-left: 3px;
                }}

                .artsasa-seo-score.excellent strong {{
                    color: #2e6b43;
                }}

                .artsasa-seo-score.very-good strong {{
                    color: #557347;
                }}

                .artsasa-seo-score.good strong {{
                    color: #8a6a28;
                }}

                .artsasa-seo-score.needs-work strong {{
                    color: #a15c3b;
                }}

                .artsasa-seo-score.poor strong {{
                    color: #9b3f36;
                }}

                .artsasa-seo-rating {{
                    margin-top: 7px;
                    font-size: 12px;
                    color: #7c4429;
                    font-weight: 600;
                }}

                .artsasa-seo-progress {{
                    height: 7px;
                    background: #e4dfd5;
                    border-radius: 20px;
                    overflow: hidden;
                    margin: 22px 0;
                }}

                .artsasa-seo-progress-bar {{
                    height: 100%;
                    background: #a15c3b;
                    border-radius: inherit;
                    transition: width .3s ease;
                }}

                .artsasa-seo-metrics {{
                    display: grid;
                    grid-template-columns:
                        repeat(4, minmax(0, 1fr));
                    border-top: 1px solid #ddd7cc;
                    border-bottom: 1px solid #ddd7cc;
                    margin-bottom: 25px;
                }}

                .artsasa-seo-metrics > div {{
                    padding: 16px;
                    border-right: 1px solid #ddd7cc;
                }}

                .artsasa-seo-metrics > div:last-child {{
                    border-right: 0;
                }}

                .artsasa-seo-metrics strong {{
                    display: block;
                    font-size: 22px;
                    font-weight: 600;
                }}

                .artsasa-seo-metrics span {{
                    display: block;
                    margin-top: 4px;
                    font-size: 10px;
                    color: #83807a;
                    text-transform: uppercase;
                    letter-spacing: .1em;
                }}

                .artsasa-seo-section {{
                    margin-top: 24px;
                }}

                .artsasa-seo-section-title {{
                    font-size: 11px;
                    text-transform: uppercase;
                    letter-spacing: .14em;
                    font-weight: 700;
                    margin-bottom: 10px;
                    color: #7c4429;
                }}

                .artsasa-seo-checks {{
                    border-top: 1px solid #ddd7cc;
                }}

                .artsasa-seo-check {{
                    display: grid;
                    grid-template-columns:
                        28px minmax(0, 1fr) auto;
                    gap: 12px;
                    align-items: start;
                    padding: 13px 0;
                    border-bottom: 1px solid #ddd7cc;
                }}

                .artsasa-seo-check-icon {{
                    width: 22px;
                    height: 22px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: 700;
                }}

                .artsasa-seo-check.pass
                .artsasa-seo-check-icon {{
                    background: #dfeade;
                    color: #2e6b43;
                }}

                .artsasa-seo-check.warning
                .artsasa-seo-check-icon {{
                    background: #f0dfd5;
                    color: #a15c3b;
                }}

                .artsasa-seo-check-title {{
                    font-weight: 700;
                    font-size: 13px;
                }}

                .artsasa-seo-check-message {{
                    margin-top: 3px;
                    color: #6f6a63;
                    font-size: 12px;
                    line-height: 1.55;
                }}

                .artsasa-seo-points {{
                    font-size: 11px;
                    color: #83807a;
                    white-space: nowrap;
                }}

                .artsasa-seo-recommendations {{
                    margin: 0;
                    padding: 0;
                    list-style: none;
                }}

                .artsasa-seo-recommendations li {{
                    display: flex;
                    flex-direction: column;
                    gap: 3px;
                    padding: 13px 0;
                    border-bottom: 1px solid #ddd7cc;
                    font-size: 12px;
                }}

                .artsasa-seo-recommendations li strong {{
                    font-size: 12px;
                }}

                .artsasa-seo-recommendations li span {{
                    color: #6f6a63;
                    line-height: 1.55;
                }}

                .artsasa-seo-all-good {{
                    color: #2e6b43;
                }}

                @media (max-width: 700px) {{

                    .artsasa-seo-panel {{
                        padding: 20px;
                    }}

                    .artsasa-seo-header {{
                        align-items: flex-start;
                    }}

                    .artsasa-seo-score strong {{
                        font-size: 34px;
                    }}

                    .artsasa-seo-metrics {{
                        grid-template-columns: repeat(2, 1fr);
                    }}

                    .artsasa-seo-metrics > div:nth-child(2) {{
                        border-right: 0;
                    }}

                    .artsasa-seo-metrics > div:nth-child(-n+2) {{
                        border-bottom: 1px solid #ddd7cc;
                    }}

                }}

            </style>
            """,
            score_class=score_class,
            score=score,
            rating=rating,
            word_count=metrics["word_count"],
            heading_count=metrics["heading_count"],
            link_count=metrics["link_count"],
            image_count=metrics["image_count"],
            checks_html=mark_safe(
                checks_html
            ),
            recommendations_html=mark_safe(
                recommendations_html
            ),
        )

    # =========================================================
    # ANALYZER HELPER
    # =========================================================

    def _run_seo_analysis(self, obj):

        return analyze_blog(

            title=obj.title or "",

            slug=obj.slug or "",

            excerpt=obj.excerpt or "",

            content=obj.content or "",

            focus_keyword=(
                getattr(
                    obj,
                    "focus_keyword",
                    ""
                )
                or ""
            ),

            seo_title=(
                obj.meta_title or ""
            ),

            meta_description=(
                obj.meta_description or ""
            ),

            featured_image=(
                obj.featured_image
                if obj.featured_image
                else None
            ),

            image_alt=(
                getattr(
                    obj,
                    "image_alt",
                    ""
                )
                or ""
            ),

        )