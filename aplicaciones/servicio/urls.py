from django.urls import path
from . import views

urlpatterns = [
    path('menu_servicio/', views.IndexView.as_view(), name='menu_servicio'),
    path('servicio_list/', views.ServicioListView.as_view(), name='servicio_list'),
    path('servicio/<int:pk>/', views.ServicioDetailView.as_view(), name='servicio_detail'),
    path('servicio_create/', views.ServicioCreateView.as_view(), name='servicio_create'),
    path('servicio_update/<int:pk>/', views.ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicio_delete/<int:pk>/', views.ServicioDeleteView.as_view(), name='servicio_delete'),
]
