from django import forms
from .models import Curso, Leccion


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'nivel']


class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'contenido', 'duracion', 'estado']