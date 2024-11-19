from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from aplicaciones.abastecimiento.models import Producto
from aplicaciones.abastecimiento.models import Stock
from aplicaciones.abastecimiento.models import Pedido
from .forms import ProductoForm, PedidoForm, StockForm
from django.db.models import F


class IndexView(TemplateView):
    template_name = 'abastecimiento/menu_principal.html'


#Vistas de producto


class ProductoListView(ListView):
    model = Producto
    template_name = 'abastecimiento/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        # Ordenar los productos por id en orden ascendente
        return Producto.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtrar los productos con cantidades fuera de los límites establecidos
        productos_limite = Producto.objects.filter(
            cantidad__lte=F('cantidad_minima')
        ) | Producto.objects.filter(
            cantidad__gte=F('cantidad_maxima')
        )
        context['productos_limite'] = productos_limite

        # Verificar si hay productos fuera del límite
        hay_productos_fuera_limite = productos_limite.exists()
        context['hay_productos_fuera_limite'] = hay_productos_fuera_limite

        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'abastecimiento/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'abastecimiento/producto_create.html'
    success_url = reverse_lazy('producto_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto agregado correctamente.')
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'abastecimiento/producto_update.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'abastecimiento/producto_delete.html'
    success_url = reverse_lazy('producto_list')


#Vista de Stock

class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'abastecimiento/stock_create.html'
    success_url = reverse_lazy('stock_list')  # Redirigir a la lista de stocks

    def form_valid(self, form):
        # Guardar el Stock
        response = super().form_valid(form)
        
        # Mensaje de éxito
        messages.success(self.request, 'Stock agregado correctamente.')
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class StockListView(ListView):
    model = Stock
    template_name = 'abastecimiento/stock_list.html'
    context_object_name = 'stocks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegúrate de que el contexto incluye todos los detalles necesarios
        context['stocks'] = Stock.objects.select_related('id_servicio').all()  # Optimiza la consulta con select_related
        return context

class StockDetailView(DetailView):
    model = Stock
    template_name = 'abastecimiento/stock_detail.html'
    context_object_name = 'stock'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegúrate de que el contexto incluye la relación del servicio
        context['stock'] = Stock.objects.select_related('id_servicio').get(pk=self.kwargs['pk'])
        return context

class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'abastecimiento/stock_delete.html'
    success_url = reverse_lazy('stock_list')

    def delete(self, request, *args, **kwargs):
        # Mensaje de confirmación después de la eliminación
        messages.success(self.request, "El stock se eliminó correctamente.")
        return super().delete(request, *args, **kwargs)

#Vista de Pedido

# Vista de Pedido
class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'abastecimiento/pedido_create.html'
    success_url = reverse_lazy('pedido_list')
    context_object_name = 'pedido'

    def get_form(self, form_class=None):
        # Obtener el formulario y modificar el queryset de id_producto
        form = super().get_form(form_class)
        form.fields['id_producto'].queryset = Producto.objects.all().order_by('id')
        return form

    def form_valid(self, form):
        # Guardar el pedido
        response = super().form_valid(form)
        
        # Actualizar la cantidad de productos en el inventario
        pedido = form.instance
        producto = pedido.id_producto
        producto.cantidad += pedido.cantidad
        producto.save()
        
        messages.success(self.request, 'Pedido creado correctamente y cantidad de producto actualizada.')
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        # Pasar la lista completa de productos al contexto para la tabla
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all().order_by('id')  # Todos los productos ordenados
        return context


class PedidoListView(ListView):
    model = Pedido
    template_name = 'abastecimiento/pedido_list.html'
    context_object_name = 'pedidos'

class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'abastecimiento/pedido_detail.html'
    context_object_name = 'pedido'