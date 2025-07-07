import django_filters
from .models import Ticket

class TicketFilter(django_filters.FilterSet):
    # Filtro para buscar texto en el título o la descripción
    query = django_filters.CharFilter(method='universal_search', label="Búsqueda General")

    class Meta:
        model = Ticket
        # Campos por los que se podrá filtrar de forma exacta
        fields = ['estado', 'nivel_critico', 'area_asignada']

    def universal_search(self, queryset, name, value):
        # Esta función permite buscar un valor en múltiples campos (título y descripción)
        return queryset.filter(
            models.Q(titulo__icontains=value) | models.Q(descripcion_problema__icontains=value)
        )
