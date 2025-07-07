from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, TicketForm, ObservacionForm, TicketUpdateForm
from .decorators import role_required
from .filters import TicketFilter
from .models import Perfil, Ticket, Observacion, Derivacion


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'core/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10 # Opcional: para paginar la lista de tickets

    def get_queryset(self):
        # Obtenemos el queryset original
        queryset = super().get_queryset().order_by('-fecha_creacion')
        # Aplicamos el filtro y devolvemos el resultado
        self.filter = TicketFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos el objeto de filtro a la plantilla
        context['filter'] = self.filter
        return context

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'core/ticket_detail.html'
    context_object_name = 'ticket'

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm # Usa el formulario que acabamos de crear
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('ticket-list') # Redirige a la lista de tickets tras la creación

    def form_valid(self, form):
        # Asigna automáticamente el usuario logueado como el creador del ticket
        form.instance.trabajador_creador = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    template_name = 'core/ticket_update_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Guardamos el área original para poder compararla después
        self.original_area = self.get_object().area_asignada
        return kwargs

    def form_valid(self, form):
        ticket = form.save(commit=False)
        motivo = form.cleaned_data.get('motivo_derivacion', '')
        
        # Comprobamos si el área ha cambiado para registrar la derivación
        if ticket.area_asignada != self.original_area:
            Derivacion.objects.create(
                ticket=ticket,
                area_origen=self.original_area,
                area_destino=ticket.area_asignada,
                trabajador_origen=self.request.user,
                motivo_derivacion=motivo if motivo else "Derivación de área."
            )
            messages.info(self.request, f'Ticket derivado al área de {ticket.area_asignada.nombre}.')

        ticket.save()
        messages.success(self.request, '¡Ticket actualizado con éxito!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket-detail', kwargs={'pk': self.object.pk})

def home_view(request):
    context = { 'project_name': 'Sistema de Tickets' }
    return render(request, 'core/welcome.html', context)


@login_required
@role_required(allowed_roles=[Perfil.Roles.JEFE_MESA])
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'core/registro.html', {'form': form})


# Vista para Ver el Detalle de un Ticket (Modificada)
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'core/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos el formulario de observaciones al contexto
        context['observacion_form'] = ObservacionForm()
        return context

    def post(self, request, *args, **kwargs):
        # Esta función maneja el envío del formulario de nueva observación
        ticket = self.get_object()
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.save(commit=False)
            observacion.ticket_asociado = ticket
            observacion.autor_trabajador = request.user
            observacion.save()
            messages.success(request, '¡Observación añadida con éxito!')
            return redirect('ticket-detail', pk=ticket.pk)
        else:
            # Si el formulario no es válido, recargamos la página con el error
            context = self.get_context_data()
            context['observacion_form'] = form
            messages.error(request, 'Hubo un error al añadir la observación.')
            return self.render_to_response(context)

# Vista para Editar un Ticket
class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    template_name = 'core/ticket_update_form.html'
    
    def get_success_url(self):
        # Redirige a la página de detalle del ticket que se acaba de actualizar
        return reverse_lazy('ticket-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, '¡Ticket actualizado con éxito!')
        return super().form_valid(form)
