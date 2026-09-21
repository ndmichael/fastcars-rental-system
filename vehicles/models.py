import os

from PIL import Image, UnidentifiedImageError

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


MAX_IMAGE_SIZE = 700 * 1024  # 700 KB
MIN_IMAGE_WIDTH = 640
MIN_IMAGE_HEIGHT = 360
MAX_IMAGE_WIDTH = 2400
MAX_IMAGE_HEIGHT = 2400

ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def validate_vehicle_year(value):
    current_year = timezone.now().year

    if value < 1980 or value > current_year + 1:
        raise ValidationError(
            f"Year must be between 1980 and {current_year + 1}."
        )


def validate_vehicle_image(file):
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image size must not exceed 700 KB."
        )

    extension = os.path.splitext(file.name)[1].lower().lstrip(".")

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            "Only JPG, JPEG, PNG, and WebP images are allowed."
        )

    try:
        image = Image.open(file)
        width, height = image.size

        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            raise ValidationError(
                f"Image must be at least "
                f"{MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT}px."
            )

        if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
            raise ValidationError(
                f"Image must not exceed "
                f"{MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT}px."
            )

        image.verify()

    except ValidationError:
        raise

    except (UnidentifiedImageError, OSError):
        raise ValidationError(
            "Upload a valid image file."
        )

    finally:
        file.seek(0)


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Vehicle(models.Model):

    CATEGORY_CHOICES = [
        ("sedan", "Sedan"),
        ("suv", "SUV"),
        ("hatchback", "Hatchback"),
        ("coupe", "Coupe"),
        ("convertible", "Convertible"),
        ("van", "Van"),
        ("pickup", "Pickup"),
    ]

    TRANSMISSION_CHOICES = [
        ("automatic", "Automatic"),
        ("manual", "Manual"),
    ]

    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("hybrid", "Hybrid"),
        ("electric", "Electric"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("maintenance", "Maintenance"),
    ]

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="vehicles",
    )

    model_name = models.CharField(
        max_length=100,
    )

    year = models.PositiveSmallIntegerField(
        validators=[validate_vehicle_year],
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    description = models.TextField(
        blank=True,
    )

    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
        ],
    )

    seats = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20),
        ],
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        db_index=True,
    )

    primary_image = models.ImageField(
        upload_to="vehicles/primary/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=ALLOWED_IMAGE_EXTENSIONS
            ),
            validate_vehicle_image,
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["brand"]),
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        super().clean()

        if self.primary_image:
            validate_vehicle_image(self.primary_image)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.year})"


class VehicleImage(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="supporting_images",
    )

    image = models.ImageField(
        upload_to="vehicles/supporting/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=ALLOWED_IMAGE_EXTENSIONS
            ),
            validate_vehicle_image,
        ],
    )

    display_order = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["vehicle", "display_order"],
                name="unique_vehicle_image_order",
            ),
        ]

    def clean(self):
        super().clean()

        if self.image:
            validate_vehicle_image(self.image)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle} - Supporting image {self.display_order}"