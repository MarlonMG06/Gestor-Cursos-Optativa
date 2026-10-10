from django.urls import path

from . import views


urlpatterns = [
    path('inicio/', views.inicio, name='home'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('cursos/', views.lista_cursos, name='cursos'),
    path('curso/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('leccion/<int:pk>/avanzar/', views.avanzar_estado_leccion, name='avanzar_estado_leccion'),
    path('', views.lista_cursos, name='lista_cursos'),

    path(
        'curso/nuevo/',
        views.crear_curso,
        name='crear_curso'
    ),

    path(
        'curso/<int:pk>/',
        views.detalle_curso,
        name='detalle_curso'
    ),

    path(
        'curso/<int:pk>/eliminar/',
        views.eliminar_curso,
        name='eliminar_curso'
    ),

    path(
        'curso/<int:pk>/leccion/nueva/',
        views.crear_leccion,
        name='crear_leccion'
    ),

    path(
        'leccion/<int:pk>/editar/',
        views.editar_leccion,
        name='editar_leccion'
    ),
    path(
        'leccion/<int:pk>/eliminar/',
        views.eliminar_leccion,
        name='eliminar_leccion'
    ),
]
