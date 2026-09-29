from django.shortcuts import render

from vehicles.models import Vehicle


def home(request):
    vehicles = (
        Vehicle.objects
        .filter(status="available")
        .select_related("brand")
        .order_by("-created_at")[:3]
    )

    return render(
        request,
        "public/home.html",
        {
            "vehicles": vehicles,
        },
    )