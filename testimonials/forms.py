from django import forms

from .models import Testimonial


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "Share your experience with FAST CARS...",
                    "rows": 5,
                }
            ),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if not message:
            raise forms.ValidationError(
                "Please enter your testimonial."
            )

        return message