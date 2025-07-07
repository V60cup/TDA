from django.urls import path
from .views import home_view, registro_view, TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView

urlpatterns = [
    
    path('', home_view, name='home'),
    path('registro/', registro_view, name='registro'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/crear/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/editar/', TicketUpdateView.as_view(), name='ticket-update'),
]