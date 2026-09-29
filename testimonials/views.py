from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TestimonialForm
from .models import Testimonial


@login_required
def create_testimonial(request):

    if request.user.role != "customer":
        messages.warning(
            request,
            "Only customer accounts can submit testimonials.",
        )
        return redirect("admin_portal:dashboard")

    if request.method == "POST":
        form = TestimonialForm(request.POST)

        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.customer = request.user
            testimonial.save()

            messages.success(
                request,
                "Your testimonial has been submitted for review.",
            )

            return redirect("testimonials:my_testimonials")

    else:
        form = TestimonialForm()

    return render(
        request,
        "customer/testimonials/create.html",
        {
            "form": form,
            "page_title": "Share Your Experience",
            "portal_label": "Customer Portal",
        },
    )


@login_required
def my_testimonials(request):
    testimonials = (
        Testimonial.objects
        .filter(customer=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "customer/testimonials/list.html",
        {
            "testimonials": testimonials,
            "page_title": "My Testimonials",
            "portal_label": "Customer Portal",
        },
    )