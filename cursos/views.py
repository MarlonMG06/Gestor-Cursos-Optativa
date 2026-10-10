<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CursoForm, LeccionForm
from .models import Curso, Leccion


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
def lista_cursos(request):
    cursos = Curso.objects.all()

    return render(
        request,
        'cursos/lista.html',
        {'cursos': cursos}
    )


<<<<<<< HEAD
@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
=======
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625

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


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
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


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
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


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
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


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
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


<<<<<<< HEAD
@login_required
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
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
<<<<<<< HEAD


@login_required
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/editar.html', {'form': form, 'curso': curso})


@login_required
@require_POST
def avanzar_estado_leccion(request, pk):
    leccion = get_object_or_404(Leccion, pk=pk)
    siguientes = {
        Leccion.ESTADO_BORRADOR: Leccion.ESTADO_REVISION,
        Leccion.ESTADO_REVISION: Leccion.ESTADO_PUBLICADO,
    }
    if leccion.estado in siguientes:
        leccion.estado = siguientes[leccion.estado]
        leccion.save(update_fields=['estado'])
    return redirect('detalle_curso', pk=leccion.curso_id)


@login_required
def inicio(request):
    return render(request, 'cursos/inicio.html')


@login_required
def acerca_de(request):
    return render(request, 'cursos/acerca_de.html')
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
