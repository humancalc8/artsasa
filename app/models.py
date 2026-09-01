from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# ARTIST
# =========================================================

class Artist(models.Model):

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="artists/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    instagram = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse(
            "artist_detail",
            kwargs={
                "slug": self.slug
            }
        )


# =========================================================
# EXHIBITION
# =========================================================

class Exhibition(models.Model):

    title = models.CharField(
        max_length=250
    )

    slug = models.SlugField(
        max_length=270,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="exhibitions/",
        blank=True,
        null=True
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    is_current = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-start_date", "-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse(
            "exhibition_detail",
            kwargs={
                "slug": self.slug
            }
        )


# =========================================================
# ARTWORK
# =========================================================

class Artwork(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Reserved", "Reserved"),
        ("Sold", "Sold"),
        ("Not for Sale", "Not for Sale"),
    ]

    EDITION_CHOICES = [
        ("Unique work", "Unique work"),
        ("Limited edition", "Limited edition"),
        ("Open edition", "Open edition"),
    ]


    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    title = models.CharField(
        max_length=250
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artworks"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artworks"
    )


    # =====================================================
    # IMAGES
    # =====================================================

    image = models.ImageField(
        upload_to="artworks/",
        blank=True,
        null=True
    )


    # =====================================================
    # DESCRIPTION
    # =====================================================

    short_description = models.TextField(
        max_length=500,
        blank=True
    )

    description = models.TextField(
        blank=True
    )


    # =====================================================
    # ARTWORK DETAILS
    # =====================================================

    medium = models.CharField(
        max_length=250,
        blank=True
    )

    year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    dimensions = models.CharField(
        max_length=200,
        blank=True
    )

    edition = models.CharField(
        max_length=100,
        choices=EDITION_CHOICES,
        default="Unique work"
    )


    # =====================================================
    # PRICE
    # =====================================================

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    currency = models.CharField(
        max_length=10,
        default="KES"
    )


    # =====================================================
    # AVAILABILITY
    # =====================================================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Available"
    )


    # =====================================================
    # EXHIBITION
    # =====================================================

    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artworks"
    )


    # =====================================================
    # WEBSITE CONTROL
    # =====================================================

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )


    # =====================================================
    # SEO
    # =====================================================

    meta_title = models.CharField(
        max_length=250,
        blank=True
    )

    meta_description = models.CharField(
        max_length=320,
        blank=True
    )


    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse(
            "product_detail",
            kwargs={
                "slug": self.slug
            }
        )


# =========================================================
# ADDITIONAL ARTWORK PHOTOS
# =========================================================

class ArtworkImage(models.Model):

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="artworks/gallery/"
    )

    caption = models.CharField(
        max_length=250,
        blank=True
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "sort_order",
            "created_at"
        ]

    def __str__(self):

        return f"{self.artwork.title} — Image"


# =========================================================
# ENQUIRY
# =========================================================

class ArtworkEnquiry(models.Model):

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} — {self.artwork.title}"
# =========================================================
# ORDER
# =========================================================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Payment Pending", "Payment Pending"),
        ("Paid", "Paid"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    # -----------------------------------------------------
    # ORDER IDENTIFICATION
    # -----------------------------------------------------

    order_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    # -----------------------------------------------------
    # CUSTOMER INFORMATION
    # -----------------------------------------------------

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50
    )

    country = models.CharField(
        max_length=100,
        default="Kenya"
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # ORDER TOTAL
    # -----------------------------------------------------

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        default="KES"
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.order_number:

            last_order = (
                Order.objects
                .order_by("-id")
                .first()
            )

            if last_order:
                next_number = last_order.id + 1
            else:
                next_number = 1

            self.order_number = (
                f"ART-{next_number:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.order_number} — {self.name}"
        )


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )

    # Snapshot of artwork information at checkout
    title = models.CharField(
        max_length=250
    )

    artist_name = models.CharField(
        max_length=200,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        default="KES"
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):

        return (
            f"{self.title} — {self.order.order_number}"
        )