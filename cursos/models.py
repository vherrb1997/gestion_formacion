from django.db import models
from profesores.models import Profesor
from django.core.exceptions import ValidationError


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    profesor = models.ForeignKey(
        Profesor, on_delete=models.PROTECT, related_name="cursos"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    plazas = models.PositiveIntegerField(default=20)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="cursos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha final no puedeser anterior a la inicial")

    def __str__(self):
        return self.nombre
