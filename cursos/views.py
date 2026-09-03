from django.shortcuts import get_object_or_404, redirect, render

from .forms import CursoForm, LeccionForm
from .models import Curso, Leccion


def lista_cursos(request):
    cursos = Curso.objects.all()

    return render(
        request,
        'cursos/lista.html',
        {'cursos': cursos}
    )


def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()

    return render(
        request,
        'cursos/crear.html',
        {'form': form}
    )


def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    lecciones = curso.lecciones.order_by('fecha_creacion')

    return render(
        request,
        'cursos/detalle.html',
        {
            'curso': curso,
            'lecciones': lecciones
        }
    )


def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    if request.method == 'POST':
        curso.delete()
        return redirect('lista_cursos')

    return render(
        request,
        'cursos/eliminar_curso.html',
        {
            'curso': curso,
            'total_lecciones': curso.lecciones.count()
        }
    )


def crear_leccion(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    if request.method == 'POST':
        form = LeccionForm(request.POST)

        if form.is_valid():
            leccion = form.save(commit=False)
            leccion.curso = curso
            leccion.save()

            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = LeccionForm()

    return render(
        request,
        'cursos/crear_leccion.html',
        {
            'form': form,
            'curso': curso
        }
    )


def editar_leccion(request, pk):
    leccion = get_object_or_404(Leccion, pk=pk)

    if request.method == 'POST':
        form = LeccionForm(request.POST, instance=leccion)

        if form.is_valid():
            form.save()
            return redirect(
                'detalle_curso',
                pk=leccion.curso.pk
            )
    else:
        form = LeccionForm(instance=leccion)

    return render(
        request,
        'cursos/editar_leccion.html',
        {
            'form': form,
            'leccion': leccion
        }
    )


def eliminar_leccion(request, pk):
    leccion = get_object_or_404(Leccion, pk=pk)

    if request.method == 'POST':
        curso_pk = leccion.curso.pk
        leccion.delete()

        return redirect(
            'detalle_curso',
            pk=curso_pk
        )

    return render(
        request,
        'cursos/eliminar_leccion.html',
        {'leccion': leccion}
    )
