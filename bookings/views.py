from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.models import Vehicle

from .forms import BookingForm
from .models import Booking


def check_availability(request, vehicle_id):
    if request.method != "GET":
        return JsonResponse(
            {"message": "GET request required."},
            status=405,
        )

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
    )

    form = BookingForm(
        request.GET,
        vehicle=vehicle,
    )

    if not form.is_valid():
        errors = {
            field: [str(error) for error in errors_list]
            for field, errors_list in form.errors.items()
        }

        return JsonResponse(
            {
                "available": False,
                "errors": errors,
            },
            status=400,
        )

    pickup_date = form.cleaned_data["pickup_date"]
    return_date = form.cleaned_data["return_date"]

    rental_days = (return_date - pickup_date).days
    total_amount = vehicle.daily_rate * rental_days

    return JsonResponse(
        {
            "available": True,
            "rental_days": rental_days,
            "daily_rate": str(vehicle.daily_rate),
            "total_amount": str(total_amount),
            "message": "Vehicle is available for your selected dates.",
        }
    )


@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
    )

    if request.method != "POST":
        return redirect("vehicles:detail", pk=vehicle.pk)

    form = BookingForm(
        request.POST,
        vehicle=vehicle,
    )

    if form.is_valid():
        booking = form.save(commit=False)
        booking.customer = request.user
        booking.vehicle = vehicle
        booking.save()

        return redirect(
            "bookings:confirmation",
            pk=booking.pk,
        )

    return render(
        request,
        "public/vehicle_detail.html",
        {
            "vehicle": vehicle,
            "booking_form": form,
        },
        status=400,
    )


@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "vehicle",
            "vehicle__brand",
            "customer",
        ),
        pk=pk,
        customer=request.user,
    )

    return render(
        request,
        "customer/booking_confirmation.html",
        {
            "booking": booking,
        },
    )