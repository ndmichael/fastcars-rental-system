from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from vehicles.models import Vehicle
from bookings.models import Booking
from testimonials.models import Testimonial
from enquiries.models import Enquiry


class Command(BaseCommand):
    help = "Create realistic FAST CARS demo data"

    def handle(self, *args, **kwargs):

        # ---------------------------------------------------------
        # 1. CREATE ADMIN USERS
        # ---------------------------------------------------------
        admin_users = [
            ("admin", "Admin User", "admin@fastcars.com"),
            ("manager", "Fleet Manager", "manager@fastcars.com"),
        ]

        for username, first_name, email in admin_users:
            User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "email": email,
                    "role": "admin",
                    "is_staff": True,
                    "is_active": True,
                },
            )

        # ---------------------------------------------------------
        # 2. CREATE CUSTOMER USERS
        # ---------------------------------------------------------
        customers = [
            ("johnsmith", "John", "Smith"),
            ("danielokafor", "Daniel", "Okafor"),
            ("emekaobi", "Emeka", "Obi"),
            ("davidadams", "David", "Adams"),
            ("michaelbrown", "Michael", "Brown"),
            ("chinedueze", "Chinedu", "Eze"),
            ("abdullahi", "Abdullahi", "Musa"),
            ("victoriajames", "Victoria", "James"),
            ("gracewilliams", "Grace", "Williams"),
            ("sarahjohnson", "Sarah", "Johnson"),
            ("oluwaseun", "Oluwaseun", "Adeyemi"),
            ("ibrahimali", "Ibrahim", "Ali"),
            ("charlesokoro", "Charles", "Okoro"),
            ("preciousobi", "Precious", "Obi"),
            ("josephdaniels", "Joseph", "Daniels"),
            ("maryann", "Mary", "Ann"),
            ("favourchukwu", "Favour", "Chukwu"),
            ("henrycole", "Henry", "Cole"),
            ("stephenudo", "Stephen", "Udo"),
            ("aminaumar", "Amina", "Umar"),
        ]

        created_customers = []

        for username, first_name, last_name in customers:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{username}@example.com",
                    "role": "customer",
                    "phone_number": "08000000000",
                    "is_active": True,
                },
            )

            if created:
                user.set_password("Password123!")
                user.save()

            created_customers.append(user)

        # ---------------------------------------------------------
        # 3. GET AVAILABLE VEHICLES
        # ---------------------------------------------------------
        vehicles = list(
            Vehicle.objects.filter(status="available")[:10]
        )

        if not vehicles:
            self.stdout.write(
                self.style.ERROR(
                    "No available vehicles found. Add vehicles first."
                )
            )
            return

        # ---------------------------------------------------------
        # 4. CREATE BOOKINGS
        # ---------------------------------------------------------
        booking_statuses = [
            "pending",
            "pending",
            "pending",
            "pending",
            "pending",
            "pending",
            "confirmed",
            "confirmed",
            "confirmed",
            "confirmed",
            "confirmed",
            "confirmed",
            "active",
            "active",
            "completed",
            "completed",
            "completed",
            "completed",
            "cancelled",
            "cancelled",
        ]

        today = timezone.localdate()

        for index, status in enumerate(booking_statuses):

            customer = created_customers[index % len(created_customers)]
            vehicle = vehicles[index % len(vehicles)]

            pickup_date = today + timedelta(days=30 + (index * 3))
            return_date = pickup_date + timedelta(days=3)

            # Completed bookings use dates in the past.
            if status == "completed":
                pickup_date = today - timedelta(days=30 + index)
                return_date = pickup_date + timedelta(days=3)

            booking, created = Booking.objects.get_or_create(
                customer=customer,
                vehicle=vehicle,
                pickup_date=pickup_date,
                return_date=return_date,
                defaults={
                    "status": status,
                },
            )

            if created:
                self.stdout.write(
                    f"Created booking {booking.reference}"
                )

        # ---------------------------------------------------------
        # 5. CREATE TESTIMONIALS
        # ---------------------------------------------------------
        testimonial_messages = [
            "The booking process was simple and straightforward.",
            "The vehicle was clean and ready when I arrived.",
            "I had a smooth experience using FAST CARS.",
            "The vehicle information was clear and helpful.",
            "The booking confirmation process was easy to understand.",
            "Great experience from booking to vehicle pickup.",
            "The platform made it easy to choose a suitable vehicle.",
            "I would use the service again.",
            "The customer portal was easy to navigate.",
            "The rental process was convenient.",
        ]

        for index, message in enumerate(testimonial_messages):
            customer = created_customers[index % len(created_customers)]

            Testimonial.objects.get_or_create(
                customer=customer,
                message=message,
                defaults={
                    "status": "active" if index < 7 else "inactive"
                },
            )

        # ---------------------------------------------------------
        # 6. CREATE ENQUIRIES
        # ---------------------------------------------------------
        enquiries = [
            ("John Smith", "john@example.com", "Vehicle availability"),
            ("Sarah Johnson", "sarah@example.com", "Luxury vehicle enquiry"),
            ("Daniel Okafor", "daniel@example.com", "Booking question"),
            ("Grace Williams", "grace@example.com", "Rental information"),
            ("David Adams", "david@example.com", "Vehicle enquiry"),
            ("Victoria James", "victoria@example.com", "Booking information"),
            ("Emeka Obi", "emeka@example.com", "Rental duration"),
            ("Amina Umar", "amina@example.com", "Vehicle availability"),
            ("Charles Okoro", "charles@example.com", "General enquiry"),
            ("Mary Ann", "mary@example.com", "Booking support"),
        ]

        enquiry_statuses = [
            "new",
            "new",
            "new",
            "new",
            "read",
            "read",
            "read",
            "resolved",
            "resolved",
            "resolved",
        ]

        for index, (name, email, subject) in enumerate(enquiries):
            Enquiry.objects.get_or_create(
                email=email,
                subject=subject,
                defaults={
                    "name": name,
                    "phone_number": "08000000000",
                    "message": (
                        f"Hello, I would like more information "
                        f"about {subject.lower()}."
                    ),
                    "status": enquiry_statuses[index],
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "FAST CARS demo data created successfully."
            )
        )