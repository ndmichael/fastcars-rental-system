from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.admin_views import admin_required

from .models import Testimonial


@admin_required
def testimonial_list(request):
    testimonials = (
        Testimonial.objects
        .select_related("customer")
        .order_by("-created_at")
    )

    return render(
        request,
        "admin/testimonials/list.html",
        {
            "testimonials": testimonials,
            "page_title": "Testimonials",
            "portal_label": "Admin Portal",
        },
    )


@admin_required
def testimonial_toggle_status(request, pk):
    if request.method != "POST":
        return redirect("admin_portal:testimonial_list")

    testimonial = get_object_or_404(Testimonial, pk=pk)

    if testimonial.status == Testimonial.Status.ACTIVE:
        testimonial.status = Testimonial.Status.INACTIVE
        message = "Testimonial has been deactivated."
    else:
        testimonial.status = Testimonial.Status.ACTIVE
        message = "Testimonial has been activated."

    testimonial.save(update_fields=["status", "updated_at"])

    messages.success(request, message)

    return redirect("admin_portal:testimonial_list")