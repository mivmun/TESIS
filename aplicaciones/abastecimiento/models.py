from django.db import models
from aplicaciones.servicio.models import Servicio

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    cantidad_minima = models.IntegerField()
    cantidad_maxima = models.IntegerField()

    def str(self):
        return f"{self.id} - {self.nombre_producto}"

class Stock(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad_necesaria = models.IntegerField()

    def str(self):
        return f"Existe {self.id_producto.cantidad} de {self.id_producto.nombre_producto}"


class Pedido(models.Model):
    id_producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad= models.IntegerField()
    monto_producto=models.IntegerField()
    empleado=models.CharField(max_length=100) #quien hace el pedido
    fecha_entrega=models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Pedido {self.id} hecho por {self.empleado}"