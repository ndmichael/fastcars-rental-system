from django.urls import path

from . import views


app_name = "testimonials"


urlpatterns = [
    path(
        "create/",
        views.create_testimonial,
        name="create",
    ),
    path(
        "my-testimonials/",
        views.my_testimonials,
        name="my_testimonials",
    ),
]