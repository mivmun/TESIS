from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from aplicaciones.servicio.models import Servicio
from .forms import ServicioForm
from django.urls import reverse_lazy 
from django.contrib import messages
from aplicaciones.reserva.models import Reserva
from django.db.models import F
from datetime import timedelta



class IndexView(TemplateView):
    template_name = 'servicio/menu_servicio.html'
    
#vistas de servicio
    

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/servicio_create.html'
    success_url = reverse_lazy('servicio_list')

    def form_valid(self, form):
        # Obtener el valor de duración del formulario
        duracion_str = form.cleaned_data['duracion']
        
        # Convertir la duración de formato HH:MM:SS a un objeto timedelta
        horas, minutos, segundos = map(int, duracion_str.split(":"))
        duracion = timedelta(hours=horas, minutes=minutos, seconds=segundos)

        # Asignar la duración convertida al objeto Servicio
        servicio = form.save(commit=False)
        servicio.duracion = duracion
        servicio.save()

        messages.success(self.request, 'Servicio agregado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'servicio/servicio_detail.html'
    context_object_name = 'servicio'

    def get_form(self):
        # Usamos el formulario con los campos deshabilitados
        form = ServicioForm(instance=self.get_object())
        return form
    
class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/servicio_update.html'
    success_url = reverse_lazy('servicio_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Servicio actualizado correctamente.')
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio/servicio_list.html'
    context_object_name = 'servicios'

    def get_queryset(self):
        return Servicio.objects.all().order_by('id')
    
class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'servicio/servicio_delete.html'
    success_url = reverse_lazy('servicio_list')
    