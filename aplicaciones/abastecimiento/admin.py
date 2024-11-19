from django.contrib import admin
from .models import Producto
from .models import Stock
from .models import Pedido


admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(Pedido)