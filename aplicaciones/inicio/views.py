from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView,DeleteView, View
from django.contrib.auth import authenticate
from .models import Empleado, Cliente
from django.contrib import messages
from aplicaciones.inicio.forms import EmpleadoForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from aplicaciones.inicio.forms import EmpleadoLoginForm, ClienteLoginForm, ClienteRegistroForm, PerfilForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin



def index(request):
    return render(request, 'inicio/index.html')

def index_servicio(request):
    return render(request, 'inicio/index_servicio.html')


def menu_empleado(request):
    return render(request, 'inicio/menu_empleado.html')

class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'inicio/empleado_form.html'
    success_url = reverse_lazy('empleado_list') 

    def get_form_class(self):
        from .forms import EmpleadoForm  # Importación diferida aquí
        return EmpleadoForm
    
class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'inicio/empleado_list.html'
    context_object_name = 'empleados'

class EmpleadoEditView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'inicio/empleado_form.html'  # Usamos el mismo formulario que para crear
    success_url = reverse_lazy('empleado_list')  # Redirige a la lista de empleados después de la actualización

    def form_valid(self, form):
        # Lógica adicional para guardar el empleado
        empleado = form.save(commit=False)
        empleado.save()
        messages.success(self.request, "Empleado actualizado correctamente.")
        return redirect(self.success_url)
    
class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'inicio/empleado_delete.html'  # Plantilla para confirmar eliminación
    success_url = reverse_lazy('empleado_list')  # Redirige a la lista de empleados

    def delete(self, request, *args, **kwargs):
        # Aquí también puedes agregar lógica de confirmación si lo necesitas
        messages.success(self.request, "Empleado eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
    

def menu_admin_empleado(request):
    return render(request, 'inicio/menu_admin_empleado.html')


class EmpleadoLoginView(View):
    def get(self, request):
        form = EmpleadoLoginForm()
        return render(request, 'inicio/login_empleado.html', {'form': form})

    def post(self, request):
        form = EmpleadoLoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            contrasena = form.cleaned_data['contrasena']

            # Autenticación de empleado usando RUT y contraseña
            empleado = authenticate(request, rut=rut, password=contrasena)

            if empleado is not None:
                login(request, empleado)
                print("Empleado autenticado y logueado")
                return redirect('menu_empleado')  
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")

        # Si el formulario no es válido o las credenciales son incorrectas
        return render(request, 'inicio/login_empleado.html', {'form': form})
    


    #CLIENTE

class ClienteRegistroView(View):
    def get(self, request):
        form = ClienteRegistroForm()
        return render(request, 'inicio/registro.html', {'form': form})

    def post(self, request):
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        return render(request, 'inicio/registro.html', {'form': form})

class ClienteLoginView(View):
    def get(self, request):
        form = ClienteLoginForm()
        return render(request, 'inicio/login.html', {'form': form})

    def post(self, request):
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            contrasena = form.cleaned_data['contrasena']

            # Verifica las credenciales del cliente
            cliente = authenticate(request, rut=rut, password=contrasena)

            if cliente is not None:
                login(request, cliente)
                return render(request, 'inicio/menu_cliente.html')
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")
        # Si el formulario no es válido o las credenciales son incorrectas
        return render(request, 'inicio/login.html', {'form': form})


class PerfilView(LoginRequiredMixin, View):
    login_url = '/login/'  

    def get(self, request):
        # Asegúrate de que el usuario esté autenticado antes de continuar
        if not request.user.is_authenticated:
            return redirect('login')  # Redirige a login si no está autenticado

        form = PerfilForm(instance=request.user)
        return render(request, 'inicio/perfil.html', {'form': form})

    def post(self, request):
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return redirect('login')  # Redirige a login si no está autenticado
        
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('menu_cliente')  # Redirige al menú cliente o donde necesites
        return render(request, 'inicio/perfil.html', {'form': form})



@login_required
def menu_cliente(request):
    form = PerfilForm(instance=request.user)
    return render(request, 'inicio/menu_cliente.html', {'form': form})

#DASHBOARD
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from aplicaciones.abastecimiento.models import Stock
from aplicaciones.reserva.models import Reserva, Agenda, Pago
from .models import Empleado
from aplicaciones.servicio.models import Servicio

class DashboardDataView(View):
    def get(self, request):
        try:
            # Indicador 1: Tasa de Ocupación
            tasa_ocupacion = (
                Reserva.objects.filter(estado_reserva='c').count() /
                Agenda.objects.filter(disponible=False).count()
            ) * 100

            # Indicador 2: Reservas por Servicio
            reservas_por_servicio = Reserva.objects.values('id_servicio__tipo_servicio').annotate(total=Count('id'))

            # Indicador 3: Tasa de Pago
            tasa_pago = (Pago.objects.filter(estado_pago='pagado').count() / Reserva.objects.count()) * 100

            # Indicador 4: Crecimiento de Reservas
            crecimiento_reservas = Reserva.objects.annotate(
                month=TruncMonth('id_agenda__fecha')
            ).values('month').annotate(total=Count('id'))

            # Indicador 5: Productos Más Utilizados
            productos_utilizados = Stock.objects.values('id_producto__nombre_producto').annotate(total_usado=Sum('cantidad_necesaria'))

            # Indicador 6: Costos por Servicio
            costos_por_servicio = Servicio.objects.annotate(
            costo_insumos=Sum(F('stock__cantidad_necesaria') * F('stock__id_producto__cantidad')),
            ).values('tipo_servicio', 'costo_insumos')

            # Respuesta JSON
            data = {
                'tasa_ocupacion': tasa_ocupacion,
                'reservas_por_servicio': list(reservas_por_servicio),
                'tasa_pago': tasa_pago,
                'crecimiento_reservas': list(crecimiento_reservas),
                'productos_utilizados': list(productos_utilizados),
                'costos_por_servicio': list(costos_por_servicio),
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DashboardView(View):
    def get(self, request):
        return render(request, 'inicio/dashboard.html')