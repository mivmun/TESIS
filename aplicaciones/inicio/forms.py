from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import CreateView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django import forms
from .models import Empleado, Cliente

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['rut','nombre', 'apellido', 'correo_electronico', 'contrasena', 'cargo', 'salario']

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si el empleado ya existe, hacer que rut sea de solo lectura
            self.fields['rut'].widget.attrs['readonly'] = True

class EmpleadoLoginForm(forms.Form):
    rut = forms.CharField(label="RUT", max_length=9, required=True)
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        contrasena = cleaned_data.get("contrasena")

        # Validación de autenticación
        empleado = authenticate(rut=rut, password=contrasena)
        if not empleado:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data 
    

#CLIENTE

class ClienteRegistroForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo_electronico', 'contrasena']
    
    rut= forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'RUT sin puntos ni guion | si termian en K Utilize "0"'})
    )

    contrasena= forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Utilize Mayusculas, Minusculas, numeros y simbolos'})
    )


    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if len(rut) > 9:
            raise forms.ValidationError("El RUT no puede tener más de 9 caracteres.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
        
        if contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class ClienteLoginForm(forms.Form):
    rut = forms.CharField(max_length=9, label="RUT", required=True)
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if len(rut) > 9:
            raise forms.ValidationError("El RUT no puede tener más de 9 caracteres.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        contrasena = cleaned_data.get("contrasena")
        
        # Autenticación del cliente
        cliente = authenticate(rut=rut, password=contrasena)
        if not cliente:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo_electronico']