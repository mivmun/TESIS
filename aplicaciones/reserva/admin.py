from django.contrib import admin
from .models import Reserva
from .models import Agenda
from .models import Pago


admin.site.register(Reserva)
admin.site.register(Agenda)
admin.site.register(Pago)