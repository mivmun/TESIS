from django import forms
from aplicaciones.inicio.models import Cliente, Empleado
from aplicaciones.reserva.models import Reserva, Agenda 
from aplicaciones.servicio.models import Servicio
from django.utils import timezone
from django.views.generic import ListView


class ReservaForm(forms.ModelForm):
    rut = forms.CharField(
        max_length=12,
        label="RUT del Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT del cliente'})
    )
    id_servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        label="Servicio",
        help_text="Selecciona el servicio que deseas reservar",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['rut', 'id_servicio', 'sector', 'direccion', 'vehiculo']
        widgets = {
            'sector': forms.TextInput(attrs={'placeholder': 'Ingresa el sector', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingresa la dirección', 'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not Cliente.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ingresado no existe en la base de datos.")
        return rut






class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['id_empleado', 'fecha', 'hora', 'disponible']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'id_empleado': forms.Select(attrs={'class': 'form-control'}),
        }
        
#gestiona la agenda de los empleados
class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['fecha', 'hora', 'id_empleado', 'disponible']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'id_empleado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'fecha': 'Fecha',
            'hora': 'Hora',
            'id_empleado': 'Empleado Responsable',
            'disponible': '¿Está disponible?',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        id_empleado = cleaned_data.get('id_empleado')

        # Validación para evitar duplicados
        if Agenda.objects.filter(fecha=fecha, hora=hora, id_empleado=id_empleado).exists():
            raise forms.ValidationError("Ya existe una disponibilidad para este empleado en esta fecha y hora.")
        return cleaned_data
    

class DisponibilidadEmpleadoForm(forms.Form):
    rut = forms.CharField(
        max_length=12,
        label="RUT del Empleado",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT del empleado'})
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de inicio de la semana"
    )
    dias = forms.MultipleChoiceField(
        choices=[
            ('lunes', 'Lunes'),
            ('martes', 'Martes'),
            ('miercoles', 'Miércoles'),
            ('jueves', 'Jueves'),
            ('viernes', 'Viernes'),
            ('sabado', 'Sábado'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Días de la semana"
    )
    horas = forms.MultipleChoiceField(
        choices=[
            ('09:00', '09:00'),
            ('10:00', '10:00'),
            ('11:00', '11:00'),
            ('12:00', '12:00'),
            ('13:00', '13:00'),
            ('14:00', '14:00'),
            ('15:00', '15:00'),
            ('16:00', '16:00'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Horas disponibles"
    )

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not Empleado.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ingresado no pertenece a un empleado registrado.")
        return rut
    
    
class FiltroEmpleadoForm(forms.Form):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        label="Seleccione un empleado",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,  # Permitir que el campo sea opcional
    )
    
    
from django import forms
from aplicaciones.reserva.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['banco', 'numero_transaccion', 'monto_abonado']
        widgets = {
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'numero_transaccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de transacción'}),
            'monto_abonado': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),  # Solo lectura
        }
        labels = {
            'banco': 'Seleccione el banco',
            'numero_transaccion': 'Número de transacción',
            'monto_abonado': 'Monto a abonar',
        }
