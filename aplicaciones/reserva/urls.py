from django.urls import path
from .views import (CrearReservaView, 
                    ReservaConfirmadaView, 
                    ValidarRutView, 
                    CrearDisponibilidadView, 
                    ListarDisponibilidadView,
                    ReservaListClientesView,
                    MenuReservaView,
                    CrearDisponibilidadEmpleadoView,
                    ValidarRutEmpleadoView,
                    CalendarioReservasView,
                    ObtenerHorasDisponiblesView,
                    PagoConfirmadaView)
from . import views

app_name = 'reserva'

urlpatterns = [
    path('crear_reserva/', CrearReservaView.as_view(), name='crear_reserva'),
    path('reserva_confirmada/', ReservaConfirmadaView.as_view(), name='reserva_confirmada'),
    path('pago_confirmado/', PagoConfirmadaView.as_view(), name='pago_confirmado'),
    path('validar_rut/', ValidarRutView.as_view(), name='validar_rut'),
    path('mis_reservas/', ReservaListClientesView.as_view(), name='reserva_list_clientes'),
    path('crear_disponibilidad/', CrearDisponibilidadView.as_view(), name='crear_disponibilidad'),
    path('listar_disponibilidad/', ListarDisponibilidadView.as_view(), name='listar_disponibilidad'),
    path('menu_reserva/', MenuReservaView.as_view(), name='menu_reserva'),
    path('crear_disponibilidad_empleado/', CrearDisponibilidadEmpleadoView.as_view(), name='crear_disponibilidad_empleado'),
    path('validar_rut_empleado/', ValidarRutEmpleadoView.as_view(), name='validar_rut_empleado'),
    path('pagar/<int:reserva_id>/', views.PagarReservaView.as_view(), name='pagar_reserva'),
    path('calendario_reservas/', CalendarioReservasView.as_view(), name='calendario_reservas'),
    path('horas_disponibles/', ObtenerHorasDisponiblesView.as_view(), name='horas_disponibles'),
]
