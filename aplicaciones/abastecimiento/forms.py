from django import forms
from aplicaciones.abastecimiento.models import Producto, Stock, Pedido
from aplicaciones.inicio.models import Empleado
from aplicaciones.servicio.models import Servicio

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id','nombre_producto', 'unidad_medida', 'cantidad', 'cantidad_minima', 'cantidad_maxima']

class PedidoForm(forms.ModelForm):
    id_producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), label='Empleado')

    class Meta:
        model = Pedido
        fields = ['id_producto', 'cantidad', 'monto_producto', 'empleado']


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['id_producto', 'id_servicio', 'cantidad_necesaria']

    # Modificar el campo id_producto para mostrar nombre y unidad de medida
    id_producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(), 
        label="Producto",
        required=True,
        empty_label="Seleccione un producto",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    id_servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(), 
        label="Servicio",
        required=True,
        empty_label="Seleccione un servicio",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cantidad_necesaria = forms.IntegerField(
        label="Cantidad Necesaria", 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # Personalización del display de productos con su unidad de medida
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        # Personalizar cómo se muestran los productos
        self.fields['id_producto'].queryset = Producto.objects.all()
        self.fields['id_producto'].widget = forms.Select(
            choices=[(producto.id, f"{producto.nombre_producto} - {producto.unidad_medida}") for producto in Producto.objects.all()]
        )
