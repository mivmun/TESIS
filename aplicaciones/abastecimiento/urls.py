from django.urls import path
from . import views
from .views import IndexView



urlpatterns = [
    path('menu_abastecimiento/', IndexView.as_view(), name='menu_principal'),
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/nuevo/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('stock/crear/', views.StockCreateView.as_view(), name='stock_create'),
    path('stocks/', views.StockListView.as_view(), name='stock_list'),
    path('stocks/<int:pk>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('stocks/<int:pk>/eliminar/', views.StockDeleteView.as_view(), name='stock_delete'),
]
