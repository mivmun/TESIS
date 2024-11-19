from django.urls import path
from . import views
from aplicaciones.inicio.views import EmpleadoCreateView, EmpleadoListView, EmpleadoLoginView, ClienteLoginView, ClienteRegistroView, PerfilView, DashboardView
from django.contrib.auth.views import LogoutView
from .views import DashboardDataView, DashboardView
from templates.inicio import *
from templates.reserva import *

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.index_servicio, name='index_servicio'),
    path('menu_admin_empleado/', views.menu_admin_empleado, name='menu_admin_empleado'),
    path('empleado_create/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado_list/', EmpleadoListView.as_view(), name='empleado_list'), 
    path('empleado_edit/<int:pk>/', views.EmpleadoEditView.as_view(), name='empleado_edit'),  # Ruta para editar
    path('empleado_delete/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),
    path('login_empleado/', EmpleadoLoginView.as_view(), name='login_empleado'),
    path('menu_empleado/', views.menu_empleado, name='menu_empleado'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', ClienteRegistroView.as_view(), name='registro'),
    path('login/', ClienteLoginView.as_view(), name='login'),
    path('menu_cliente/', views.menu_cliente, name='menu_cliente'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('dashboard/api/', DashboardDataView.as_view(), name='dashboard_api'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

