from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, TicketForm
from .decorators import role_required
from .models import Perfil, Ticket


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'core/ticket_list.html' # Usaremos esta nueva plantilla
    context_object_name = 'tickets'
    ordering = ['-fecha_creacion'] # Ordenar por fecha de creación descendente

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