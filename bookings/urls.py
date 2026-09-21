from django.urls import path

from . import views


app_name = "bookings"

urlpatterns = [
    path(
        "vehicle/<int:vehicle_id>/availability/",
        views.check_availability,
        name="check_availability",
    ),
    path(
        "vehicle/<int:vehicle_id>/book/",
        views.create_booking,
        name="create",
    ),
    path(
        "<int:pk>/confirmation/",
        views.booking_confirmation,
        name="confirmation",
    ),
]