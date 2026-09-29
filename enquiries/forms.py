from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry

        fields = [
            "name",
            "email",
            "phone_number",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "Your name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "Optional",
                    "autocomplete": "tel",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "What can we help you with?",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "Write your enquiry...",
                    "rows": 6,
                }
            ),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_subject(self):
        return self.cleaned_data["subject"].strip()

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if not message:
            raise forms.ValidationError(
                "Please enter your enquiry."
            )

        return message