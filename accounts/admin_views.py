from django.contrib.auth import get_user_model
from django.shortcuts import render

from vehicles.admin_views import admin_required


User = get_user_model()


@admin_required
def customer_list(request):
    customers = (
        User.objects
        .filter(role="customer")
        .order_by("-date_joined")
    )

    return render(
        request,
        "admin/customers/list.html",
        {
            "customers": customers,
            "page_title": "Customers",
            "portal_label": "Admin Portal",
        },
    )