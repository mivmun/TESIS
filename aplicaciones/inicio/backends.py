from django.contrib.auth.backends import BaseBackend
from aplicaciones.inicio.models import Cliente ,Empleado
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from aplicaciones.inicio.forms import PerfilForm


class ClienteBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None):
        try:
            cliente = Cliente.objects.get(rut=rut)
            if check_password(password, cliente.contrasena):
                # Retorna el cliente sin modificar last_login
                return cliente
            return None
        except Cliente.DoesNotExist:
            return None
        


@login_required
def menu_cliente(request):
    cliente = request.user  # Usuario autenticado
    form = PerfilForm(instance=cliente)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('inicio:menu_cliente')

    return render(request, 'menu_cliente.html', {'form': form})





#EMPLEADO
class EmpleadoBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        try:
            empleado = Empleado.objects.get(rut=rut)
            if empleado and check_password(password, empleado.contrasena):
                return empleado
        except Empleado.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Empleado.objects.get(pk=user_id)
        except Empleado.DoesNotExist:
            return None


