from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST


def registro(request):
    datos = {}
    errors = []

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        datos = request.POST

        if not username:
            errors.append('El nombre de usuario es obligatorio.')
        if not email:
            errors.append('El correo electrónico es obligatorio.')
        if password1 != password2:
            errors.append('Las contraseñas no coinciden.')
        if User.objects.filter(username=username).exists():
            errors.append('El nombre de usuario ya existe.')
        if User.objects.filter(email=email).exists():
            errors.append('El correo electrónico ya está registrado.')

        if not errors:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/registro.html', {'errors': errors, 'datos': datos})


def es_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_admin)
def grupos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_grupo', '').strip()
        if nombre and not Group.objects.filter(name=nombre).exists():
            Group.objects.create(name=nombre)
        return redirect('grupos')

    return render(request, 'accounts/grupos.html', {'grupos': Group.objects.all().order_by('name')})


@user_passes_test(es_admin)
@require_POST
def eliminar_grupo(request, id_grupo):
    grupo = get_object_or_404(Group, id=id_grupo)
    grupo.delete()
    return redirect('grupos')


def dar_miembros(grupo):
    return grupo.user_set.all().order_by('username')


def dar_no_miembros(grupo):
    miembros = dar_miembros(grupo)
    return User.objects.exclude(id__in=miembros.values_list('id', flat=True)).order_by('username')


@user_passes_test(es_admin)
def editar_grupo(request, id_grupo):
    grupo = get_object_or_404(Group, id=id_grupo)

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('name', '').strip()
        if nuevo_nombre and not Group.objects.exclude(id=grupo.id).filter(name=nuevo_nombre).exists():
            grupo.name = nuevo_nombre
            grupo.save(update_fields=['name'])
        return redirect('editar_grupo', id_grupo=grupo.id)

    return render(
        request,
        'accounts/editar_grupo.html',
        {
            'grupo': grupo,
            'miembros': dar_miembros(grupo),
            'no_miembros': dar_no_miembros(grupo),
        },
    )


@user_passes_test(es_admin)
@require_POST
def agregar_usuario_grupo(request, id_grupo):
    grupo = get_object_or_404(Group, id=id_grupo)
    id_user = request.POST.get('id_user')
    if id_user:
        user = get_object_or_404(User, id=id_user)
        grupo.user_set.add(user)
    return redirect('editar_grupo', id_grupo=grupo.id)


@user_passes_test(es_admin)
@require_POST
def eliminar_usuario_grupo(request, id_grupo):
    grupo = get_object_or_404(Group, id=id_grupo)
    id_user = request.POST.get('id_user')
    if id_user:
        user = get_object_or_404(User, id=id_user)
        grupo.user_set.remove(user)
    return redirect('editar_grupo', id_grupo=grupo.id)


@user_passes_test(es_admin)
def permisos(request):
    grupos = Group.objects.all().order_by('name')
    permisos = Permission.objects.select_related('content_type').order_by(
        'content_type__app_label', 'content_type__model', 'codename'
    )

    grupo_id = request.POST.get('grupo') if request.method == 'POST' else request.GET.get('grupo')
    grupo = get_object_or_404(Group, id=grupo_id) if grupo_id else grupos.first()

    if request.method == 'POST' and grupo:
        permisos_ids = request.POST.getlist('permisos')
        grupo.permissions.set(permisos_ids)
        return redirect(f"{reverse('permisos')}?grupo={grupo.id}")

    permisos_grupo = set()
    if grupo:
        permisos_grupo = set(grupo.permissions.values_list('id', flat=True))

    return render(
        request,
        'accounts/permisos.html',
        {
            'permisos': permisos,
            'grupos': grupos,
            'grupo': grupo,
            'permisos_grupo': permisos_grupo,
        },
    )
