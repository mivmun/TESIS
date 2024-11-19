from django.db import models
from aplicaciones.inicio.models import Empleado
from datetime import timedelta



class Servicio(models.Model):
    tipo_servicio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    modalidad_servicio_choices = [
        ('Taller', 'Taller'), 
        ('Domicilio', 'Domicilio'),
    ]
    modalidad_servicio = models.CharField(
        max_length=10,
        choices=modalidad_servicio_choices,
        default='Taller',
    )
    valor = models.CharField(max_length=20)
    duracion = models.DurationField(default=timedelta(hours=1))

    def __str__(self):
        return self.tipo_servicio

class Categoria(models.Model):
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)  
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nivel_categoria_choices = [
        ('basico', 'Básico'),
        ('medio', 'Medio'),
        ('premium', 'Premium'),
    ]
    nivel_categoria = models.CharField(
        max_length=10,
        choices=nivel_categoria_choices,
        default='basico',
    )

    def __str__(self):
        return f"{self.id_empleado.nombre} - {self.id_servicio.tipo_servicio} ({self.nivel_categoria})"

