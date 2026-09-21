from django.shortcuts import get_object_or_404, render

from .models import Vehicle


def vehicle_list(request):
    vehicles = (
        Vehicle.objects
        .select_related("brand")
        .prefetch_related("supporting_images")
        .filter(status="available")
    )

    return render(
        request,
        "public/cars.html",
        {"vehicles": vehicles},
    )


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(
        Vehicle.objects
        .select_related("brand")
        .prefetch_related("supporting_images"),
        pk=pk,
    )

    return render(
        request,
        "public/vehicle_detail.html",
        {"vehicle": vehicle},
    )
