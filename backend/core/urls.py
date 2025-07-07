from django.urls import path
from .views import (
    welcome_view,
    registro_view,
    login_view,
    logout_view,
    PerfilDetailView, 
    PerfilUpdateView,
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    TicketDeleteView
)

urlpatterns = [
    # Ruta principal
    path('', welcome_view, name='home'),
    path('perfil/', PerfilDetailView.as_view(), name='perfil-detail'),

    # Rutas de autenticación
    path('registro/', registro_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('perfil/', PerfilDetailView.as_view(), name='perfil-detail'),
    path('perfil/editar/', PerfilUpdateView.as_view(), name='perfil-update'),


    # Rutas de Tickets (CRUD)
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/nuevo/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/editar/', TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/eliminar/', TicketDeleteView.as_view(), name='ticket-delete'),
]