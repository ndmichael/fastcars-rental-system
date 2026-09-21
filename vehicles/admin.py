from django.contrib import admin
from django.utils.html import format_html

from .models import Brand, Vehicle, VehicleImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "vehicle_count", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Vehicles")
    def vehicle_count(self, obj):
        return obj.vehicles.count()


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 0
    max_num = 3
    min_num = 0
    fields = ("image", "display_order", "preview")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj.image:
            return "—"

        return format_html(
            '<img src="{}" width="120" height="75" '
            'style="object-fit:cover;border-radius:6px;" />',
            obj.image.url,
        )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_name",
        "brand",
        "category",
        "daily_rate",
        "seats",
        "transmission",
        "fuel_type",
        "status",
        "created_at",
    )

    list_filter = (
        "brand",
        "category",
        "transmission",
        "fuel_type",
        "status",
    )

    search_fields = (
        "model_name",
        "brand__name",
        "description",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "primary_image_preview",
    )

    fields = (
        "brand",
        "model_name",
        "year",
        "category",
        "description",
        "daily_rate",
        "seats",
        "transmission",
        "fuel_type",
        "status",
        "primary_image",
        "primary_image_preview",
        "created_at",
        "updated_at",
    )

    inlines = [VehicleImageInline]

    @admin.display(description="Vehicle")
    def vehicle_name(self, obj):
        return f"{obj.brand.name} {obj.model_name}"

    @admin.display(description="Primary image")
    def primary_image_preview(self, obj):
        if not obj.primary_image:
            return "—"

        return format_html(
            '<img src="{}" width="180" height="110" '
            'style="object-fit:cover;border-radius:8px;" />',
            obj.primary_image.url,
        )


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "display_order",
        "created_at",
    )

    list_filter = (
        "display_order",
    )

    search_fields = (
        "vehicle__model_name",
        "vehicle__brand__name",
    )

    ordering = (
        "vehicle",
        "display_order",
    )

    readonly_fields = ("created_at", "preview")

    fields = (
        "vehicle",
        "image",
        "display_order",
        "preview",
        "created_at",
    )

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj.image:
            return "—"

        return format_html(
            '<img src="{}" width="180" height="110" '
            'style="object-fit:cover;border-radius:8px;" />',
            obj.image.url,
        )