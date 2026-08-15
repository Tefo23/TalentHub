from django import forms
from .models import Job
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ["cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Explain why you are a great fit for this role...",
                }
            ),
        }

class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            "title",
            "description",
            "requirements",
            "location",
            "employment_type",
            "salary_min",
            "salary_max",
            "deadline",
			"status",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Junior Python Developer",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe the job opportunity...",
                }
            ),

            "requirements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "List the skills, qualifications and experience required...",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Gaborone",
                }
            ),

            "employment_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ), 
			"jobstatus": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "salary_min": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "5000",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "salary_max": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "8000",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }