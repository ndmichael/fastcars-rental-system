from django.urls import path

from . import views
from vehicles import admin_views as vehicle_admin_views
from bookings import admin_views as booking_admin_views
from testimonials import admin_views as testimonial_admin_views
from enquiries import admin_views as enquiry_admin_views

from accounts import admin_views as account_admin_views

app_name = "admin_portal"

urlpatterns = [
    path("", views.admin_dashboard, name="dashboard"),

    # Brands
    path(
        "brands/",
        vehicle_admin_views.brand_list,
        name="brand_list",
    ),
    path(
        "brands/add/",
        vehicle_admin_views.brand_create,
        name="brand_create",
    ),
    path(
        "brands/<int:pk>/edit/",
        vehicle_admin_views.brand_edit,
        name="brand_edit",
    ),
    path(
        "brands/<int:pk>/delete/",
        vehicle_admin_views.brand_delete,
        name="brand_delete",
    ),
    # Vehicles
    path(
        "vehicles/",
        vehicle_admin_views.vehicle_list,
        name="vehicle_list",
    ),
    path(
        "vehicles/add/",
        vehicle_admin_views.vehicle_create,
        name="vehicle_create",
    ),
    path(
        "vehicles/<int:pk>/edit/",
        vehicle_admin_views.vehicle_edit,
        name="vehicle_edit",
    ),
    path(
        "bookings/",
        booking_admin_views.booking_list,
        name="booking_list",
    ),
    path(
        "bookings/<str:reference>/",
        booking_admin_views.booking_detail,
        name="booking_detail",
    ),

    path(
        "bookings/<str:reference>/confirm/",
        booking_admin_views.booking_confirm,
        name="booking_confirm",
    ),

    path(
        "bookings/<str:reference>/cancel/",
        booking_admin_views.booking_cancel,
        name="booking_cancel",
    ),

    path(
        "bookings/<str:reference>/activate/",
        booking_admin_views.booking_activate,
        name="booking_activate",
    ),

    path(
        "bookings/<str:reference>/complete/",
        booking_admin_views.booking_complete,
        name="booking_complete",
    ),

    path(
        "testimonials/",
        testimonial_admin_views.testimonial_list,
        name="testimonial_list",
    ),

    path(
        "testimonials/<int:pk>/toggle-status/",
        testimonial_admin_views.testimonial_toggle_status,
        name="testimonial_toggle_status",
    ),
    path(
        "enquiries/",
        enquiry_admin_views.enquiry_list,
        name="enquiry_list",
    ),

    path(
        "enquiries/<int:pk>/status/",
        enquiry_admin_views.enquiry_update_status,
        name="enquiry_update_status",
    ),

    path(
        "customers/",
        account_admin_views.customer_list,
        name="customer_list",
    ),
]