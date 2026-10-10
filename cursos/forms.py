from django import forms
from .models import Curso, Leccion


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
<<<<<<< HEAD
        fields = ['titulo', 'descripcion', 'nivel', 'imagen']
=======
        fields = ['titulo', 'descripcion', 'nivel']
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625


class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
<<<<<<< HEAD
        fields = ['titulo', 'contenido', 'duracion', 'estado', 'prioridad']
=======
        fields = ['titulo', 'contenido', 'duracion', 'estado']
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
