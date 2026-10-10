from django.db import models


class Curso(models.Model):

    NIVEL_PRINCIPIANTE = 'Principiante'
    NIVEL_INTERMEDIO = 'Intermedio'
    NIVEL_AVANZADO = 'Avanzado'

    NIVELES = [
        (NIVEL_PRINCIPIANTE, 'Principiante'),
        (NIVEL_INTERMEDIO, 'Intermedio'),
        (NIVEL_AVANZADO, 'Avanzado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(
        max_length=20,
        choices=NIVELES,
        default=NIVEL_PRINCIPIANTE
    )

<<<<<<< HEAD
    imagen = models.ImageField(upload_to='cursos/', blank=True)

=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
    def __str__(self):
        return self.titulo


class Leccion(models.Model):

    ESTADO_BORRADOR = 'Borrador'
<<<<<<< HEAD
    ESTADO_REVISION = 'En revision'
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
    ESTADO_PUBLICADO = 'Publicado'

    ESTADOS = [
        (ESTADO_BORRADOR, 'Borrador'),
<<<<<<< HEAD
        (ESTADO_REVISION, 'En revisión'),
=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
        (ESTADO_PUBLICADO, 'Publicado'),
    ]

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='lecciones'
    )

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    duracion = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_BORRADOR
    )

<<<<<<< HEAD
    PRIORIDADES = [('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta')]
    prioridad = models.CharField(max_length=5, choices=PRIORIDADES, default='MEDIA')

=======
>>>>>>> 5f3720524fe05cf11850da46746ec79b8d439625
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo