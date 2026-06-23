from django import forms
from .models import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = "__all__"

    widgets = {
        "nombre": forms.TextInput(attrs={"class": "form-control"}),
    }
