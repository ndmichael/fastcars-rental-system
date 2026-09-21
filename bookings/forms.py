from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["pickup_date", "return_date"]

        widgets = {
            "pickup_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control fc-form-control",
                }
            ),
            "return_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control fc-form-control",
                }
            ),
        }

    def __init__(self, *args, vehicle=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vehicle = vehicle

    def clean(self):
        cleaned_data = super().clean()

        pickup_date = cleaned_data.get("pickup_date")
        return_date = cleaned_data.get("return_date")

        if not pickup_date or not return_date:
            return cleaned_data

        today = timezone.localdate()

        if pickup_date < today:
            self.add_error(
                "pickup_date",
                "Pick-up date cannot be in the past.",
            )

        if return_date <= pickup_date:
            self.add_error(
                "return_date",
                "Return date must be after the pick-up date.",
            )

        if self.vehicle:
            if self.vehicle.status != "available":
                raise ValidationError(
                    "This vehicle is currently unavailable for booking."
                )

            conflicting_bookings = Booking.objects.filter(
                vehicle=self.vehicle,
                status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED,
                ],
                pickup_date__lt=return_date,
                return_date__gt=pickup_date,
            )

            if self.instance.pk:
                conflicting_bookings = conflicting_bookings.exclude(
                    pk=self.instance.pk
                )

            if conflicting_bookings.exists():
                raise ValidationError(
                    "This vehicle is already booked for part of the selected period."
                )

        return cleaned_data