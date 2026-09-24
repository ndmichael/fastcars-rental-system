from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone

from bookings.models import Booking

from django.contrib import messages
from .forms import ProfileForm

from .models import User
from bookings.models import Booking
from vehicles.models import Vehicle


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def register_view(request):
    if request.user.is_authenticated:
        return redirect("pages:home")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            messages.success(
                request,
                "Your FAST CARS account has been created.",
            )

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("pages:home")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "next": next_url or "",
        },
    )



@login_required
def dashboard_view(request):
    if request.user.role != "customer":
        return redirect("pages:home")

    bookings = (
        Booking.objects
        .filter(customer=request.user)
        .select_related("vehicle")
        .order_by("-created_at")
    )

    stats = bookings.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        confirmed=Count("id", filter=Q(status="confirmed")),
        completed=Count("id", filter=Q(status="completed")),
    )

    upcoming_booking = (
        bookings
        .filter(
            status="confirmed",
            pickup_date__gte=timezone.localdate(),
        )
        .order_by("pickup_date")
        .first()
    )

    return render(
        request,
        "customer/dashboard.html",
        {
            "page_title": "Dashboard",
            "portal_label": "Customer Portal",
            "stats": stats,
            "recent_bookings": bookings[:5],
            "upcoming_booking": upcoming_booking,
        },
    )


@login_required
def profile_view(request):
    if request.user.role != "customer":
        return redirect("pages:home")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.strip().lower()
            user.save()

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "customer/profile.html",
        {
            "form": form,
            "page_title": "Profile",
            "portal_label": "Customer Portal",
        },
    )



@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("pages:home")

    customers = User.objects.filter(role="customer")

    stats = {
        "customers": customers.count(),
        "vehicles": Vehicle.objects.count(),
        "available_vehicles": Vehicle.objects.filter(status="available").count(),
        "pending_bookings": Booking.objects.filter(status="pending").count(),
        "confirmed_bookings": Booking.objects.filter(status="confirmed").count(),
        "completed_bookings": Booking.objects.filter(status="completed").count(),
    }

    recent_bookings = (
        Booking.objects
        .select_related("customer", "vehicle")
        .order_by("-created_at")[:8]
    )

    return render(
        request,
        "admin/dashboard.html",
        {
            "page_title": "Dashboard",
            "portal_label": "Admin Portal",
            "stats": stats,
            "recent_bookings": recent_bookings,
        },
    )