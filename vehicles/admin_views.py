from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BrandForm
from .models import Brand

from .forms import BrandForm, VehicleForm
from .models import Brand, Vehicle


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if request.user.role != "admin":
            return redirect("pages:home")

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def brand_list(request):
    query = request.GET.get("q", "").strip()

    brands = (
        Brand.objects
        .annotate(vehicle_count=Count("vehicles"))
        .order_by("name")
    )

    if query:
        brands = brands.filter(
            Q(name__icontains=query)
        )

    return render(
        request,
        "admin/brands/list.html",
        {
            "brands": brands,
            "query": query,
            "page_title": "Brands",
            "portal_label": "Admin Portal",
        },
    )


@admin_required
def brand_create(request):
    if request.method == "POST":
        form = BrandForm(request.POST)

        if form.is_valid():
            brand = form.save()

            messages.success(
                request,
                f"{brand.name} has been added successfully.",
            )

            return redirect("admin_portal:brand_list")
    else:
        form = BrandForm()

    return render(
        request,
        "admin/brands/form.html",
        {
            "form": form,
            "page_title": "Add Brand",
            "portal_label": "Admin Portal",
            "form_title": "Add brand",
            "form_description": "Create a vehicle brand for your fleet.",
            "submit_label": "Add brand",
        },
    )


@admin_required
def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)

    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)

        if form.is_valid():
            brand = form.save()

            messages.success(
                request,
                f"{brand.name} has been updated successfully.",
            )

            return redirect("admin_portal:brand_list")
    else:
        form = BrandForm(instance=brand)

    return render(
        request,
        "admin/brands/form.html",
        {
            "form": form,
            "brand": brand,
            "page_title": f"Edit {brand.name}",
            "portal_label": "Admin Portal",
            "form_title": "Edit brand",
            "form_description": "Update the vehicle brand details.",
            "submit_label": "Save changes",
        },
    )


@admin_required
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)

    if request.method != "POST":
        return redirect("admin_portal:brand_list")

    try:
        brand.delete()

        messages.success(
            request,
            f"{brand.name} has been deleted successfully.",
        )

    except ProtectedError:
        messages.error(
            request,
            f"{brand.name} cannot be deleted because vehicles are "
            "currently associated with it.",
        )

    return redirect("admin_portal:brand_list")


@admin_required
def vehicle_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()

    vehicles = (
        Vehicle.objects
        .select_related("brand")
        .order_by("-created_at")
    )

    if query:
        vehicles = vehicles.filter(
            Q(model_name__icontains=query)
            | Q(brand__name__icontains=query)
        )

    if status:
        vehicles = vehicles.filter(status=status)

    if category:
        vehicles = vehicles.filter(category=category)

    return render(
        request,
        "admin/vehicles/list.html",
        {
            "vehicles": vehicles,
            "query": query,
            "status": status,
            "category": category,
            "status_choices": Vehicle.STATUS_CHOICES,
            "category_choices": Vehicle.CATEGORY_CHOICES,
            "page_title": "Vehicles",
            "portal_label": "Admin Portal",
        },
    )


@admin_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)  

        if form.is_valid():
            vehicle = form.save()

            # Attach the supporting images to the newly created vehicle.
            # supporting_images = formset.save(commit=False)

            messages.success(
                request,
                f"{vehicle} has been added successfully.",
            )

            return redirect("admin_portal:vehicle_list")
    else:
        form = VehicleForm()

    return render(
        request,
        "admin/vehicles/form.html",
        {
            "form": form,
            "page_title": "Add Vehicle",
            "portal_label": "Admin Portal",
            "form_title": "Add vehicle",
            "form_description": "Add a vehicle to your FAST CARS fleet.",
            "submit_label": "Add vehicle",
        },
    )


@admin_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(
        Vehicle.objects.select_related("brand"),
        pk=pk,
    )

    if request.method == "POST":
        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle,
        )

        if form.is_valid():
            vehicle = form.save()

            messages.success(
                request,
                f"{vehicle} has been updated successfully.",
            )

            return redirect(
                "admin_portal:vehicle_list"
            )

    else:
        form = VehicleForm(instance=vehicle)

    return render(
        request,
        "admin/vehicles/form.html",
        {
            "form": form,
            "vehicle": vehicle,
            "page_title": f"Edit {vehicle}",
            "portal_label": "Admin Portal",
            "form_title": "Edit vehicle",
            "form_description": (
                "Update this vehicle's fleet information."
            ),
            "submit_label": "Save changes",
        },
    )