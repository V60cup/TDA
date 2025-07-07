from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ticket, Perfil, User
from .forms import TicketForm, ObservacionForm, UserUpdateForm
from .filters import TicketFilter

# VISTA DE BIENVENIDA
def welcome_view(request):
    """Renderiza la página de bienvenida estática."""
    return render(request, 'core/welcome.html')

# VISTAS DE AUTENTICACIÓN
def registro_view(request):
    """Maneja el registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def login_view(request):
    """Maneja el inicio de sesión de los usuarios."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

# VISTAS PARA TICKETS (BASADAS EN CLASES)
class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'core/ticket_list.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aseguramos que el queryset se pase al filtro
        queryset = self.get_queryset()
        context['filter'] = TicketFilter(self.request.GET, queryset=queryset)
        # Pasamos el queryset filtrado a la plantilla
        context['tickets'] = context['filter'].qs
        return context

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'core/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['observacion_form'] = ObservacionForm()
        return context

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Ticket creado exitosamente.')
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'core/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        messages.success(self.request, 'Ticket actualizado exitosamente.')
        return super().form_valid(form)

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'core/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ticket eliminado exitosamente.')
        return super().form_valid(form)
    
class PerfilDetailView(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = 'core/perfil_detail.html'
    context_object_name = 'perfil'

    def get_object(self):
        """
        Devuelve el perfil del usuario actualmente logueado,
        en lugar de buscar uno por PK en la URL.
        """
        return self.request.user.perfil
    
class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'core/perfil_form.html'
    success_url = reverse_lazy('perfil-detail')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):

        messages.success(self.request, '¡Tu perfil ha sido actualizado exitosamente!')
        return super().form_valid(form)