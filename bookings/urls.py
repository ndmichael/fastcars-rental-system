from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path(
        "check-availability/<int:vehicle_id>/",
        views.check_availability,
        name="check_availability",
    ),
    path(
        "create/<int:vehicle_id>/",
        views.create_booking,
        name="create_booking",
    ),
    path("confirmation/<str:reference>/", views.booking_confirmation, name="booking_confirmation"),
    path(
        "my-bookings/<str:reference>/",
        views.booking_detail,
        name="booking_detail",
    ),
]