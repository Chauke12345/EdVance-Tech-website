from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


from .models import ProjectRequest


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = [
            'service',
            'business_name',
            'project_title',
            'description',
            'budget',
            'preferred_completion_date',
            'supporting_document',
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'placeholder': 'Your business name (optional)'
            }),
            'project_title': forms.TextInput(attrs={
                'placeholder': 'Give your project a name'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what you want EdVance Tech to develop...',
                'rows': 6
            }),
            'preferred_completion_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }
