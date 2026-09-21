import uuid
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def generate_booking_reference():
    return f"FC-{uuid.uuid4().hex[:8].upper()}"


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    reference = models.CharField(
        max_length=11,
        unique=True,
        editable=False,
        default=generate_booking_reference,
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    pickup_date = models.DateField()
    return_date = models.DateField()

    rate_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        editable=False,
    )

    rental_days = models.PositiveIntegerField(
        editable=False,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        editable=False,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["customer", "status"]),
            models.Index(fields=["vehicle", "status"]),
            models.Index(fields=["pickup_date", "return_date"]),
        ]

    def clean(self):
        super().clean()

        if self.pickup_date and self.return_date:
            if self.return_date <= self.pickup_date:
                raise ValidationError({
                    "return_date": "Return date must be after the pick-up date."
                })

        if self.vehicle_id and self.pickup_date and self.return_date:
            conflicting_bookings = Booking.objects.filter(
                vehicle_id=self.vehicle_id,
                status__in=[
                    self.Status.PENDING,
                    self.Status.CONFIRMED,
                ],
                pickup_date__lt=self.return_date,
                return_date__gt=self.pickup_date,
            )

            if self.pk:
                conflicting_bookings = conflicting_bookings.exclude(
                    pk=self.pk
                )

            if conflicting_bookings.exists():
                raise ValidationError(
                    "This vehicle already has a pending or confirmed booking "
                    "for part of the selected rental period."
                )

        if self.vehicle_id and not self.rate_per_day:
            self.rate_per_day = self.vehicle.daily_rate

        if self.pickup_date and self.return_date:
            self.rental_days = (self.return_date - self.pickup_date).days

            if self.rate_per_day:
                self.total_amount = (
                    self.rate_per_day * self.rental_days
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.customer.username}"