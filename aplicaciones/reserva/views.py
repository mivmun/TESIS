from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, FormView, ListView
from .forms import ReservaForm, DisponibilidadForm, PagoForm
from aplicaciones.servicio.models import Servicio
from aplicaciones.reserva.models import Reserva, Agenda
from aplicaciones.inicio.models import Cliente, Empleado
from django.http import JsonResponse
import json
from django.http import HttpResponseNotFound
from .forms import AgendaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.db import transaction
from .forms import DisponibilidadEmpleadoForm, FiltroEmpleadoForm
from datetime import datetime, timedelta
from django.contrib import messages
from django import forms



class MenuReservaView(TemplateView):
    template_name = 'reserva/menu_reserva.html'



#RESERVAAAAAAAAA
from datetime import datetime

class CrearReservaView(View):
    def get(self, request):
        form = ReservaForm()
        return render(request, 'reserva/crear_reserva.html', {'form': form})

    def post(self, request):
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Asegura consistencia
                    reserva = form.save(commit=False)  # Crea la reserva sin guardar aún

                    # Validar y obtener el cliente por el RUT ingresado
                    rut = form.cleaned_data.get('rut')
                    cliente = Cliente.objects.filter(rut=rut).first()
                    if not cliente:
                        form.add_error('rut', "No se encontró un cliente con el RUT ingresado.")
                        return render(request, 'reserva/crear_reserva.html', {'form': form})

                    reserva.id_cliente = cliente  # Asignar el cliente a la reserva

                    # Validar y asociar la disponibilidad seleccionada
                    fecha = request.POST.get('fecha')  # Obtener la fecha seleccionada desde el formulario
                    hora = request.POST.get('hora')    # Obtener la hora seleccionada desde el formulario

                    if not fecha or not hora:
                        form.add_error(None, "Debe seleccionar una fecha y hora disponibles.")
                        return render(request, 'reserva/crear_reserva.html', {'form': form})

                    agenda = Agenda.objects.filter(fecha=fecha, hora=hora, disponible=True).first()

                    if not agenda:
                        form.add_error(None, "La disponibilidad seleccionada ya no está disponible.")
                        return render(request, 'reserva/crear_reserva.html', {'form': form})

                    agenda.disponible = False  # Marcar la agenda como no disponible
                    agenda.save()

                    reserva.id_agenda = agenda
                    reserva.save()

                    # Lógica para bloquear los horarios adicionales
                    self.bloquear_horarios(reserva)

                messages.success(request, "Reserva creada con éxito.")
                return redirect('reserva:reserva_confirmada')

            except Exception as e:
                form.add_error(None, f"Ocurrió un error al procesar la reserva: {str(e)}")

        return render(request, 'reserva/crear_reserva.html', {'form': form})

    def bloquear_horarios(self, reserva):
        """
        Bloquea los horarios adicionales en la tabla Agenda según la duración del servicio.
        """
        # Duración del servicio ya es un timedelta
        duracion_servicio = reserva.id_servicio.duracion
        agenda = reserva.id_agenda

        # Calcular la hora de finalización
        hora_inicio = agenda.hora
        hora_fin = (datetime.combine(agenda.fecha, hora_inicio) + duracion_servicio).time()

        # Filtrar horarios a bloquear en la tabla Agenda
        agendas_a_bloquear = Agenda.objects.filter(
            fecha=agenda.fecha,
            hora__gte=hora_inicio,
            hora__lt=hora_fin,
            disponible=True
        )

        # Bloquear los horarios seleccionados
        agendas_a_bloquear.update(disponible=False)

        # Depuración opcional: imprimir horarios bloqueados
        print(f"Horarios bloqueados en {agenda.fecha}: {[agenda.hora for agenda in agendas_a_bloquear]}")


class ReservaListClientesView(ListView):
    model = Reserva
    template_name = 'reserva/reserva_list_clientes.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        # Obtener el RUT del cliente desde la URL
        rut_cliente = self.request.GET.get('rut', None)
        
        if rut_cliente is None:
            raise Http404("No se ha proporcionado un RUT")
        
        try:
            cliente = Cliente.objects.get(rut=rut_cliente)  # Buscar cliente por RUT
        except Cliente.DoesNotExist:
            raise Http404("El cliente con el RUT proporcionado no existe")
        
        # Filtrar las reservas que pertenecen a ese cliente
        return Reserva.objects.filter(id_cliente=cliente).order_by('-id')

class ReservaConfirmadaView(TemplateView):
    template_name = 'reserva/reserva_confirmada.html'

class PagoConfirmadaView(TemplateView):
    template_name = 'reserva/pago_confirmado.html'

#DISPONIBILIDAD
class CrearDisponibilidadEmpleadoView(FormView):
    template_name = 'reserva/crear_disponibilidad_empleado.html'
    form_class = DisponibilidadEmpleadoForm
    success_url = reverse_lazy('reserva:listar_disponibilidad')

    def form_valid(self, form):
        rut = form.cleaned_data['rut']
        empleado = get_object_or_404(Empleado, rut=rut)

        fecha_inicio = form.cleaned_data['fecha_inicio']
        dias_seleccionados = form.cleaned_data['dias']
        horas_seleccionadas = form.cleaned_data['horas']

        dias_map = {
            'lunes': 0,
            'martes': 1,
            'miercoles': 2,
            'jueves': 3,
            'viernes': 4,
            'sabado': 5,
        }

        for dia in dias_seleccionados:
            for hora in horas_seleccionadas:
                fecha = fecha_inicio + timedelta(days=dias_map[dia])
                hora_obj = datetime.strptime(hora, "%H:%M").time()

                # Crear o actualizar la disponibilidad
                Agenda.objects.update_or_create(
                    id_empleado=empleado,
                    fecha=fecha,
                    hora=hora_obj,
                    defaults={'disponible': True}
                )

        messages.success(self.request, "Disponibilidad guardada correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return self.render_to_response(self.get_context_data(form=form))

class ListarDisponibilidadView(FormView):
    template_name = 'reserva/listar_disponibilidad.html'
    form_class = FiltroEmpleadoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado_id = self.request.GET.get('empleado')

        if empleado_id:
            agendas = Agenda.objects.filter(id_empleado=empleado_id, disponible=True).order_by('fecha', 'hora')
        else:
            agendas = Agenda.objects.none()

        context['agendas'] = agendas
        return context



class ElegirDisponibilidadView(View):
    def get(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        form = DisponibilidadForm()
        return render(request, 'reserva/elegir_disponibilidad.html', {'form': form, 'reserva': reserva})

    def post(self, request, reserva_id):
        agenda_id = request.POST.get('id_agenda')
        reserva = get_object_or_404(Reserva, id=reserva_id)

        try:
            agenda = Agenda.objects.get(id=agenda_id, disponible=True)
            agenda.disponible = False
            agenda.save()

            reserva.id_agenda = agenda
            reserva.save()

            return redirect('reserva-pago', reserva_id=reserva.id)

        except Agenda.DoesNotExist:
            return render(request, 'reserva/elegir_disponibilidad.html', {
                'form': DisponibilidadForm(),
                'reserva': reserva,
                'error': 'El horario seleccionado no está disponible.'
            })
            
class CrearDisponibilidadView(FormView):
    template_name = 'reserva/crear_disponibilidad.html'  # Plantilla a usar
    form_class = AgendaForm  # Formulario asociado
    success_url = reverse_lazy('reserva:listar_disponibilidad')  # Redirección después de guardar

    def form_valid(self, form):
        form.save()  # Guarda la instancia del modelo
        return super().form_valid(form) 

#VALIDACION
class ValidarRutEmpleadoView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)  # Obtener los datos enviados
        rut = data.get('rut')

        # Verificar si el RUT pertenece a un empleado
        if Empleado.objects.filter(rut=rut).exists():
            return JsonResponse({'valid': True, 'message': 'El RUT pertenece a un empleado registrado.'})
        else:
            return JsonResponse({'valid': False, 'message': 'El RUT ingresado no pertenece a un empleado registrado.'})

class ValidarRutView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Obtener los datos de la solicitud
            rut = data.get('rut')

            # Buscar al cliente por RUT
            cliente = Cliente.objects.get(rut=rut)
            return JsonResponse({'existe': True})

        except Cliente.DoesNotExist:
            return JsonResponse({'existe': False})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from aplicaciones.reserva.models import Reserva, Pago
from aplicaciones.servicio.models import Servicio
from .forms import PagoForm

class PagarReservaView(View):
    def get(self, request, reserva_id):
        # Obtener la reserva y el servicio asociado
        reserva = get_object_or_404(Reserva, id=reserva_id)
        servicio = reserva.id_servicio

        try:
            # Convertir el valor del servicio a float
            valor_servicio = float(servicio.valor)
        except (ValueError, TypeError):
            # Si no se puede convertir, mostrar un mensaje de error
            messages.error(request, 'El valor del servicio no es válido.')
            return redirect('reserva:reserva_list_clientes')

        # Calcular el 50% del valor del servicio
        abono = valor_servicio * 0.3

        # Crear un formulario con el monto precargado
        form = PagoForm(initial={'monto_abonado': abono})

        return render(request, 'reserva/pagar_reserva.html', {
            'servicio': servicio,
            'abono': abono,
            'form': form,
        })

    def post(self, request, reserva_id):
        # Obtener la reserva y el servicio asociado
        reserva = get_object_or_404(Reserva, id=reserva_id)
        servicio = reserva.id_servicio

        try:
            # Convertir el valor del servicio a float
            valor_servicio = float(servicio.valor)
        except (ValueError, TypeError):
            # Si no se puede convertir, mostrar un mensaje de error
            messages.error(request, 'El valor del servicio no es válido.')
            return redirect('reserva:reserva_list_clientes')

        # Calcular el 50% del valor del servicio
        abono = valor_servicio * 0.3

        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.id_reserva = reserva
            pago.servicio = servicio

            # Verificar si el monto abonado cumple con el total del servicio
            if pago.monto_abonado >= abono:
                pago.estado_pago = 'pagado'
                # Cambiar estado de la reserva a confirmado
                reserva.estado_reserva = 'c'
            else:
                pago.estado_pago = 'parcial'

            # Guardar el pago y la reserva (si necesario)
            pago.save()
            reserva.save()

            messages.success(request, 'El pago se ha realizado con éxito. ¡Reserva confirmada!')
            return redirect('reserva:reserva_confirmada')

        messages.error(request, 'Ocurrió un error al procesar el pago. Verifique los datos ingresados.')
        return render(request, 'reserva/pagar_reserva.html', {
            'servicio': servicio,
            'abono': abono,
            'form': form,
        })


from django.views.generic import TemplateView
from aplicaciones.reserva.models import Reserva

class CalendarioReservasView(TemplateView):
    template_name = 'reserva/calendario_reservas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservas = Reserva.objects.select_related('id_cliente', 'id_servicio', 'id_agenda')
        
        # Convertir las reservas en un formato compatible con FullCalendar
        eventos = []
        for reserva in reservas:
            eventos.append({
                "title": f"{reserva.id_cliente.rut} - {reserva.id_servicio.tipo_servicio}",
                "start": f"{reserva.id_agenda.fecha}T{reserva.id_agenda.hora.strftime('%H:%M')}",
                "description": (
                    f"Sector: {reserva.sector}, "
                    f"Dirección: {reserva.direccion}, "
                    f"Vehículo: {reserva.get_vehiculo_display()}, "
                    f"Estado: {reserva.get_estado_reserva_display()}"
                ),
            })
        
        context['eventos'] = eventos
        return context






class ObtenerHorasDisponiblesView(View):
    """
    Vista para devolver las horas disponibles en formato JSON
    para una fecha específica proporcionada como parámetro.
    """

    def get(self, request, *args, **kwargs):
        fecha = request.GET.get('fecha', None)

        if not fecha:
            return JsonResponse({'error': 'No se proporcionó una fecha válida.'}, status=400)

        try:
            # Convertir la fecha a formato datetime
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

            # Filtrar las horas disponibles para la fecha seleccionada
            agendas = Agenda.objects.filter(fecha=fecha_obj, disponible=True)

            # Extraer las horas como lista
            horas_disponibles = [agenda.hora.strftime('%H:%M') for agenda in agendas]

            return JsonResponse({'horas': horas_disponibles}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido.'}, status=400)





    







    
    



    

