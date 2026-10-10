from django import forms
from .models import Curso, Leccion


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'nivel', 'imagen']


class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'contenido', 'duracion', 'estado', 'prioridad']
