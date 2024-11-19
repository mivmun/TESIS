from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    rut = models.CharField(
        max_length=9,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8,9}$',
                message='Rut invalido: Si su rut termina en "K", debe reemplazarlo con un cero "0".'
            )
        ]
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo_electronico = models.EmailField(
        unique=True,
        validators=[EmailValidator(message='Ingrese un correo electrónico válido')]
    )
    contrasena = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(128),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[-_.*])(?=.*\d).{6,128}$',
                message=( 
                    'La contraseña debe tener entre 6 y 40 caracteres, '
                    'con al menos una mayúscula, '
                    'una minúscula, '
                    'un número y un símbolo permitido (-, _, ., *).'
                )
            )
        ]
    )
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Encriptar la contraseña antes de guardarla
        if self.contrasena and not self.contrasena.startswith('$'):
            # Verifica si la contraseña ya está hasheada
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.rut}'


# EMPLEADO
class Empleado(Usuario):
    cargo_choices = [
        ('basico', 'Basico'),
        ('medio', 'Medio'),
        ('premium', 'Premium'),
    ]
    cargo = models.CharField(
        max_length=10,
        choices=cargo_choices,
        default='basico'
    )
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"


# CLIENTE
class Cliente(Usuario):
    rango_choices = [
        ('f', 'Frecuente'),
        ('n', 'Nuevo'),
        ('v', 'VIP'),
    ]
    rango = models.CharField(
        max_length=1,
        choices=rango_choices,
        default='n',
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rango}" 
