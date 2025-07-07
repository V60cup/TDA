from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <-- Importa las vistas de auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # --- AÑADE ESTAS LÍNEAS ---
    # Cuando un usuario vaya a /login/, Django usará su propia vista de Login.
    # Solo necesitas decirle qué plantilla HTML debe mostrar.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # Lo mismo para el logout, que redirige a la página de login después de cerrar sesión.
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
