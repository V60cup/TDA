# core/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from .models import Perfil

def home_view(request):
    """
    Esta es la vista principal de nuestra aplicación.
    Renderiza la plantilla 'welcome.html'.
    """
    # Puedes pasar datos a la plantilla a través de un diccionario de contexto
    context = {
        'project_name': 'Sistema de Tickets',
        'current_time': 'Jueves, 19 de Junio de 2025'
    }
    return render(request, 'core/welcome.html', context)

@login_required # Primero, el usuario debe estar logueado
@role_required(allowed_roles=[Perfil.Roles.JEFE_MESA])
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('home') # Redirigir a la página principal
    else:
        form = RegistroUsuarioForm()
    return render(request, 'core/registro.html', {'form': form})