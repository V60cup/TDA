# core/views.py

from django.shortcuts import render

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