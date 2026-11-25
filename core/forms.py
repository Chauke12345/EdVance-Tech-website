from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'autocomplete': 'tel',
            }),
            'service': forms.Select(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'rows': 5,
            }),
        }

# ==========================================================
# STAFF QUOTATION FORM
# ==========================================================

from decimal import Decimal
from django import forms
from client_portal.models import ProjectRequest
from client_portal.quotation_models import Quotation


class StaffQuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            "project",
            "total_amount",
            "deposit_percentage",
            "scope_of_work",
            "terms_and_conditions",
            "valid_until",
        ]
        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "total_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "step": "0.01",
                "placeholder": "Quotation total in Rands",
            }),
            "deposit_percentage": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "max": "100",
                "step": "0.01",
            }),
            "scope_of_work": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe the work included in this quotation...",
            }),
            "terms_and_conditions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter payment terms and other conditions...",
            }),
            "valid_until": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = (
            ProjectRequest.objects
            .filter(client__is_staff=False)
            .select_related("client")
            .order_by("-created_at")
        )
        self.fields["project"].label_from_instance = (
            lambda project: (
                f"{project.project_title} — "
                f"{project.client.get_full_name() or project.client.username}"
            )
        )

    def clean_deposit_percentage(self):
        value = self.cleaned_data["deposit_percentage"]
        if value < Decimal("0") or value > Decimal("100"):
            raise forms.ValidationError(
                "Deposit percentage must be between 0 and 100."
            )
        return value
