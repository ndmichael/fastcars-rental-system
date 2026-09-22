from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = UserAdmin.fieldsets + (
        (
            "FAST CARS",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "avatar",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "FAST CARS",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "phone_number",
                    "avatar",
                )
            },
        ),
    )