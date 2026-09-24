from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.admin_views import admin_required

from .models import Booking


@admin_required
def booking_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    bookings = (
        Booking.objects
        .select_related(
            "customer",
            "vehicle",
            "vehicle__brand",
        )
        .order_by("-created_at")
    )

    if query:
        bookings = bookings.filter(
            Q(reference__icontains=query)
            | Q(customer__username__icontains=query)
            | Q(customer__email__icontains=query)
            | Q(vehicle__model_name__icontains=query)
            | Q(vehicle__brand__name__icontains=query)
        )

    if status:
        bookings = bookings.filter(status=status)

    return render(
        request,
        "admin/bookings/list.html",
        {
            "bookings": bookings,
            "query": query,
            "status": status,
            "status_choices": Booking.Status.choices,
            "page_title": "Bookings",
            "portal_label": "Admin Portal",
        },
    )


@admin_required
def booking_detail(request, reference):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "customer",
            "vehicle",
            "vehicle__brand",
        ),
        reference=reference,
    )

    return render(
        request,
        "admin/bookings/detail.html",
        {
            "booking": booking,
            "page_title": "Booking Details",
            "portal_label": "Admin Portal",
        },
    )


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

# existing imports remain...


@admin_required
def booking_confirm(request, reference):

    if request.method != "POST":
        return redirect(
            "admin_portal:booking_detail",
            reference=reference,
        )

    booking = get_object_or_404(
        Booking,
        reference=reference,
    )

    if booking.status != Booking.Status.PENDING:
        messages.warning(
            request,
            "Only pending bookings can be confirmed.",
        )
        return redirect(
            "admin_portal:booking_detail",
            reference=booking.reference,
        )

    booking.status = Booking.Status.CONFIRMED
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        f"Booking {booking.reference} has been confirmed.",
    )

    return redirect(
        "admin_portal:booking_detail",
        reference=booking.reference,
    )


@admin_required
def booking_cancel(request, reference):

    if request.method != "POST":
        return redirect(
            "admin_portal:booking_detail",
            reference=reference,
        )

    booking = get_object_or_404(
        Booking,
        reference=reference,
    )

    if booking.status not in [
        Booking.Status.PENDING,
        Booking.Status.CONFIRMED,
    ]:
        messages.warning(
            request,
            "This booking cannot be cancelled at its current status.",
        )
        return redirect(
            "admin_portal:booking_detail",
            reference=booking.reference,
        )

    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        f"Booking {booking.reference} has been cancelled.",
    )

    return redirect(
        "admin_portal:booking_detail",
        reference=booking.reference,
    )


@admin_required
def booking_activate(request, reference):

    if request.method != "POST":
        return redirect(
            "admin_portal:booking_detail",
            reference=reference,
        )

    booking = get_object_or_404(
        Booking,
        reference=reference,
    )

    if booking.status != Booking.Status.CONFIRMED:
        messages.warning(
            request,
            "Only confirmed bookings can be marked active.",
        )
        return redirect(
            "admin_portal:booking_detail",
            reference=booking.reference,
        )

    booking.status = Booking.Status.ACTIVE
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        f"Booking {booking.reference} is now active.",
    )

    return redirect(
        "admin_portal:booking_detail",
        reference=booking.reference,
    )


@admin_required
def booking_complete(request, reference):

    if request.method != "POST":
        return redirect(
            "admin_portal:booking_detail",
            reference=reference,
        )

    booking = get_object_or_404(
        Booking,
        reference=reference,
    )

    if booking.status != Booking.Status.ACTIVE:
        messages.warning(
            request,
            "Only active bookings can be completed.",
        )
        return redirect(
            "admin_portal:booking_detail",
            reference=booking.reference,
        )

    booking.status = Booking.Status.COMPLETED
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        f"Booking {booking.reference} has been completed.",
    )

    return redirect(
        "admin_portal:booking_detail",
        reference=booking.reference,
    )