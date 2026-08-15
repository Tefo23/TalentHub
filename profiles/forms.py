from django import forms
from .models import EmployerProfile
from .models import CandidateProfile

class EmployerProfileForm(forms.ModelForm):

    class Meta:
        model = EmployerProfile

        fields = [
            "company_name",
            "industry",
            "website",
            "company_logo",
            "description",
            "location",
        ]

        widgets = {
            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company name",
                }
            ),

            "industry": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Industry",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell candidates about your company...",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company location",
                }
            ),

            "company_logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
		
class CandidateProfileForm(forms.ModelForm):

  class Meta:
    model = CandidateProfile
    fields = ['headline', 'bio', 'location', 'portfolio']
    widgets = {
        'headline': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Full-Stack Django Developer',
            }
        ),
        'bio': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell employers about yourself, experience, and goals...',
            }
        ),
        'location': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Gaborone, Botswana / Remote',
            }
        ),
        'portfolio': forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com',
            }
        ),
    }