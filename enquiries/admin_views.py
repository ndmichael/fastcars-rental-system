from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.admin_views import admin_required

from .models import Enquiry


@admin_required
def enquiry_list(request):
    enquiries = (
        Enquiry.objects
        .order_by("-created_at")
    )

    return render(
        request,
        "admin/enquiries/list.html",
        {
            "enquiries": enquiries,
            "page_title": "Enquiries",
            "portal_label": "Admin Portal",
        },
    )


@admin_required
def enquiry_update_status(request, pk):
    if request.method != "POST":
        return redirect("admin_portal:enquiry_list")

    enquiry = get_object_or_404(Enquiry, pk=pk)

    status = request.POST.get("status")

    valid_statuses = {
        choice[0]
        for choice in Enquiry.Status.choices
    }

    if status not in valid_statuses:
        messages.error(
            request,
            "Invalid enquiry status.",
        )
        return redirect("admin_portal:enquiry_list")

    enquiry.status = status
    enquiry.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        f"Enquiry marked as {enquiry.get_status_display().lower()}.",
    )

    return redirect("admin_portal:enquiry_list")
