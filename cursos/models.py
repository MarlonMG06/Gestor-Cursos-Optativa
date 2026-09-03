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

    def __str__(self):
        return self.titulo


class Leccion(models.Model):

    ESTADO_BORRADOR = 'Borrador'
    ESTADO_PUBLICADO = 'Publicado'

    ESTADOS = [
        (ESTADO_BORRADOR, 'Borrador'),
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

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo