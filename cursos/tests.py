from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Curso, Leccion


class GestorCursosTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('estudiante', password='clave-de-prueba')
        self.curso = Curso.objects.create(titulo='Python', descripcion='Fundamentos')
        self.leccion = Leccion.objects.create(curso=self.curso, titulo='Variables', contenido='Introducción', duracion=15)

    def test_todas_las_vistas_requieren_sesion(self):
        rutas = [('home', []), ('acerca_de', []), ('lista_cursos', []), ('crear_curso', []),
                 ('detalle_curso', [self.curso.pk]), ('editar_curso', [self.curso.pk]),
                 ('eliminar_curso', [self.curso.pk]), ('crear_leccion', [self.curso.pk]),
                 ('editar_leccion', [self.leccion.pk]), ('eliminar_leccion', [self.leccion.pk]),
                 ('avanzar_estado_leccion', [self.leccion.pk])]
        for nombre, args in rutas:
            with self.subTest(nombre=nombre):
                url = reverse(nombre, args=args)
                self.assertRedirects(self.client.get(url), reverse('login') + '?next=' + url)
                self.assertEqual(self.client.post(url).status_code, 302)
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())
        self.leccion.refresh_from_db()
        self.assertEqual(self.leccion.estado, 'Borrador')

    def test_login_errores_destino_y_logout(self):
        response = self.client.post(reverse('login'), {'username': 'estudiante', 'password': 'incorrecta'})
        self.assertContains(response, 'errorlist')
        url = reverse('detalle_curso', args=[self.curso.pk])
        response = self.client.post(reverse('login'), {'username': 'estudiante', 'password': 'clave-de-prueba', 'next': url})
        self.assertRedirects(response, url)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_paginas_y_formularios(self):
        self.client.force_login(self.user)
        for name, args in [('home', []), ('acerca_de', []), ('lista_cursos', []), ('crear_curso', []),
                           ('detalle_curso', [self.curso.pk]), ('editar_curso', [self.curso.pk]),
                           ('eliminar_curso', [self.curso.pk]), ('crear_leccion', [self.curso.pk]),
                           ('editar_leccion', [self.leccion.pk]), ('eliminar_leccion', [self.leccion.pk])]:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)
        self.assertContains(self.client.get(reverse('lista_cursos')), reverse('crear_curso'))
        self.assertEqual(self.client.get(reverse('detalle_curso', args=[9999])).status_code, 404)

    def test_creacion_edicion_imagen_y_validacion(self):
        self.client.force_login(self.user)
        data = {'titulo': 'Django', 'descripcion': 'Desarrollo web', 'nivel': 'Principiante'}
        with TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            stream = BytesIO()
            Image.new('RGB', (16, 16), 'blue').save(stream, 'PNG')
            response = self.client.post(reverse('crear_curso'), {**data, 'imagen': SimpleUploadedFile('portada.png', stream.getvalue(), content_type='image/png')})
            self.assertRedirects(response, reverse('lista_cursos'))
            curso = Curso.objects.get(titulo='Django')
            nombre_imagen = curso.imagen.name
            self.assertTrue(curso.imagen.storage.exists(nombre_imagen))
            self.assertContains(self.client.get(reverse('detalle_curso', args=[curso.pk])), curso.imagen.url)
            response = self.client.post(reverse('editar_curso', args=[curso.pk]), {**data, 'titulo': 'Django actualizado'})
            self.assertRedirects(response, reverse('detalle_curso', args=[curso.pk]))
            curso.refresh_from_db()
            self.assertEqual(curso.imagen.name, nombre_imagen)
            self.assertEqual(curso.titulo, 'Django actualizado')
            invalid = self.client.post(reverse('crear_curso'), {**data, 'imagen': SimpleUploadedFile('falso.png', b'no es imagen')})
            self.assertEqual(invalid.status_code, 200)
            self.assertTrue(invalid.context['form'].errors)
        self.client.post(reverse('crear_curso'), data)
        self.assertEqual(Curso.objects.filter(titulo='Django').count(), 1)

    def test_prioridad_avance_y_csrf(self):
        self.client.force_login(self.user)
        url = reverse('avanzar_estado_leccion', args=[self.leccion.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.user)
        self.assertEqual(protected.post(url).status_code, 403)
        for estado in ['En revision', 'Publicado', 'Publicado']:
            self.assertRedirects(self.client.post(url), reverse('detalle_curso', args=[self.curso.pk]))
            self.leccion.refresh_from_db()
            self.assertEqual(self.leccion.estado, estado)
        response = self.client.post(reverse('crear_leccion', args=[self.curso.pk]),
            {'titulo': 'Bucles', 'contenido': 'For y while', 'duracion': 20, 'estado': 'Borrador', 'prioridad': 'ALTA'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Leccion.objects.get(titulo='Bucles').prioridad, 'ALTA')
        invalid = self.client.post(reverse('editar_leccion', args=[self.leccion.pk]),
            {'titulo': 'Variables', 'contenido': 'Texto', 'duracion': -1, 'estado': 'Publicado', 'prioridad': 'INVALIDA'})
        self.assertTrue(invalid.context['form'].errors)

    def test_eliminacion_solo_post_y_cascada(self):
        self.client.force_login(self.user)
        url = reverse('eliminar_curso', args=[self.curso.pk])
        self.client.get(url)
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())
        self.assertTrue(Leccion.objects.filter(pk=self.leccion.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('lista_cursos'))
        self.assertFalse(Curso.objects.filter(pk=self.curso.pk).exists())
        self.assertFalse(Leccion.objects.filter(pk=self.leccion.pk).exists())
