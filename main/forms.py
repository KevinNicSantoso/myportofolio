from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "year",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "year": "Tahun Pembuatan",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 200,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Tell us about your project",
                    "rows": 3,
                }
            ),
            "year": forms.TextInput(
                attrs={
                    "placeholder": "2024",
                }
            ),
        }