from django import forms

from .models import Brand, Vehicle, VehicleImage
from django.forms import inlineformset_factory


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "e.g. Toyota",
                    "autocomplete": "off",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError("Brand name is required.")

        if Brand.objects.filter(
            name__iexact=name
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "A brand with this name already exists."
            )

        return name


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "brand",
            "model_name",
            "year",
            "category",
            "description",
            "daily_rate",
            "seats",
            "transmission",
            "fuel_type",
            "status",
            "primary_image",
        )
        widgets = {
            "brand": forms.Select(
                attrs={
                    "class": "fc-form-control",
                }
            ),
            "model_name": forms.TextInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "e.g. Camry",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "2025",
                    "min": "2000",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "fc-form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "Describe the vehicle...",
                    "rows": 5,
                }
            ),
            "daily_rate": forms.NumberInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "50000.00",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "seats": forms.NumberInput(
                attrs={
                    "class": "fc-form-control",
                    "placeholder": "5",
                    "min": "1",
                    "max": "20",
                }
            ),
            "transmission": forms.Select(
                attrs={
                    "class": "fc-form-control",
                }
            ),
            "fuel_type": forms.Select(
                attrs={
                    "class": "fc-form-control",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "fc-form-control",
                }
            ),
            "primary_image": forms.ClearableFileInput(
                attrs={
                    "class": "fc-form-control",
                    "accept": ".jpg,.jpeg,.png,.webp",
                }
            ),
        }

    def clean_model_name(self):
        return self.cleaned_data["model_name"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()


class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ("image", "display_order")
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "fc-form-control",
                    "accept": ".jpg,.jpeg,.png,.webp",
                }
            ),
            "display_order": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supporting images are optional.
        self.fields["image"].required = False

    def clean(self):
        cleaned_data = super().clean()

        image = cleaned_data.get("image")

        # Only validate an image when one was uploaded.
        if image and image.size > 700 * 1024:
            self.add_error(
                "image",
                "Image must be 700 KB or smaller.",
            )

        return cleaned_data


class BaseVehicleImageFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        if not form.instance.pk:
            form.initial["display_order"] = index + 1


VehicleImageFormSet = inlineformset_factory(
    Vehicle,
    VehicleImage,
    form=VehicleImageForm,
    extra=3,
    max_num=3,
    validate_max=True,
)