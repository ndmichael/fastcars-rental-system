from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import EnquiryForm


def create_enquiry(request):

    if request.method == "POST":
        form = EnquiryForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your enquiry has been sent successfully. We'll get back to you soon.",
            )

            return redirect("enquiries:create")

    else:
        form = EnquiryForm()

    return render(
        request,
        "public/contact.html",
        {
            "form": form,
        },
    )