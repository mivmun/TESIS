from django import forms 
from aplicaciones.servicio.models import Servicio



class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['tipo_servicio', 'modalidad_servicio', 'descripcion', 'valor', 'duracion']

    # Asegúrate de usar un widget que permita ingresar horas, minutos y segundos

    valor = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Valor sin puntos ni simbolos'})
    )
    duracion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Sigue el Formato: HH:MM:SS   Ejemplo:12:30:00'})
    )



