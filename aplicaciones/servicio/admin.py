from django.contrib import admin
from .models import Servicio
from .models import Categoria


admin.site.register(Servicio)
admin.site.register(Categoria)