# aplicaciones/reserva/models.py
from django.db import models
from aplicaciones.servicio.models import Servicio, Empleado
from aplicaciones.inicio.models import Cliente  
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from aplicaciones.abastecimiento.models import Stock
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Agenda(models.Model):
    id_empleado= models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Agenda: {self.id} {self.id_empleado} - {self.fecha} {self.hora} - Disponible: {self.disponible}"


class Reserva(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)  # Relación con Servicio
    id_agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    # Información adicional: sector y dirección
    sector = models.CharField(max_length=100, blank=False)
    direccion = models.CharField(max_length=255, blank=False)

    # Opciones de vehículos
    vehiculo_choices = [
        ('c', 'City Car'), 
        ('h', 'Hatchback/Sedán'),
        ('j', 'Suv/Jeep'),
        ('xl', 'Camionetas XL')
    ]
    vehiculo = models.CharField(
        max_length=2,
        choices=vehiculo_choices,
        default='c',
    )

    # Estado de la reserva
    estado_reserva_choices = [
        ('p', 'Pendiente'),
        ('c', 'Confirmada')
    ]
    estado_reserva = models.CharField(
        max_length=2,
        choices=estado_reserva_choices,
        default='p',
    )

    def verificar_y_descontar_stock(self):

        # Obtener los productos necesarios para el servicio asociado a esta reserva
        stock_items = Stock.objects.filter(id_servicio=self.id_servicio)

        # Verificar si hay suficiente stock
        for stock in stock_items:
            producto = stock.id_producto
            if producto.cantidad < stock.cantidad_necesaria:
                raise ValidationError(
                    f"No hay suficiente stock para el producto '{producto.nombre_producto}'. "
                    f"Cantidad disponible: {producto.cantidad}, "
                    f"Cantidad requerida: {stock.cantidad_necesaria}."
                )

        # Si hay suficiente stock, descontar la cantidad necesaria
        for stock in stock_items:
            producto = stock.id_producto
            producto.cantidad -= stock.cantidad_necesaria
            producto.save()

    def bloquear_horarios_siguientes(self):
        """Bloquea los horarios posteriores en función de la duración del servicio."""
        agenda = self.id_agenda
        servicio = self.id_servicio

        # Duración del servicio en horas
        duracion = servicio.duracion  # Asegúrate de que el modelo Servicio tiene este campo

        # Calcular horarios a bloquear
        hora_inicio = agenda.hora
        fecha = agenda.fecha
        empleado = agenda.id_empleado

        for i in range(1, duracion):  # Bloquea las horas dentro de la duración
            hora_siguiente = (datetime.combine(fecha, hora_inicio) + timedelta(hours=i)).time()

            # Buscar y bloquear la siguiente hora
            Agenda.objects.filter(
                fecha=fecha,
                hora=hora_siguiente,
                id_empleado=empleado,
                disponible=True
            ).update(disponible=False)

    def confirmar_reserva(self):
        """Confirma la reserva y realiza las acciones necesarias."""
        self.estado_reserva = 'c'  # Cambiar estado a Confirmada
        self.save()  # Guardar cambios
        self.bloquear_horarios_siguientes()  # Bloquear horarios

    def save(self, *args, **kwargs):
        if not self.pk:  # Si la reserva es nueva (no existe en la base de datos)
            self.verificar_y_descontar_stock()  # Verificar y descontar stock
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva: {self.id} - {self.estado_reserva} - Sector: {self.sector} - Dirección: {self.direccion}"



    
class Pago(models.Model):
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('parcial', 'Parcial'),
    ]
    estado_pago = models.CharField(max_length=10, 
                                   choices=ESTADO_PAGO_CHOICES, 
                                   default='pendiente')
    # El banco que el cliente elige
    banco_choices = [
        ('banco BICE', 'Banco BICE'),
        ('banco Chile', 'Banco Chile - Edwards/Citi'),
        ('banco consorcio', 'Banco Consorcio'),
        ('banco estado', 'Banco Estado'),
        ('banco falabella', 'Banco Falabella'),
        ('banco HSBC', 'Banco HSBC'),
        ('banco internacional', 'Banco Internacional'),
        ('banco itau', 'Banco Itaú'),
        ('banco Security', 'Banco Security'),
        ('bci', 'Banco BCI'),
        ('santander', 'Banco Santander'),
        ('scotiabank', 'Banco Scotiabank'),
        ('otro', 'Otro')
    ]
    banco = models.CharField(max_length=50, choices=banco_choices)
    numero_transaccion = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return f"Abono de {self.monto_abonado} por el servicio {self.servicio} - Reserva {self.id_reserva.id}"
