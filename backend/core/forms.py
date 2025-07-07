# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Area, Ticket, Cliente, Observacion

class RegistroUsuarioForm(UserCreationForm):

    rol = forms.ChoiceField(choices=Perfil.Roles.choices, required=True)
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
   
    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        # Opcional: para que los campos de nombre y email sean requeridos
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        # Aquí puedes añadir lógica adicional antes de guardar
        if commit:
            user.save()
            # Creamos el perfil asociado
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            perfil.rol = self.cleaned_data.get('rol')
            perfil.area = self.cleaned_data.get('area')
            perfil.save()
        return user
    
class TicketForm(forms.ModelForm):
    # Hacemos que la selección de cliente y área sea más amigable
    cliente_solicitante = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label="Cliente Solicitante",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area_asignada = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        label="Área Asignada",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Ticket
        # Campos que se mostrarán en el formulario de creación
        fields = [
            'titulo', 
            'descripcion_problema', 
            'cliente_solicitante',
            'nivel_critico',
            'tipo_problema',
            'area_asignada',
        ]
        # Etiquetas personalizadas para los campos
        labels = {
            'titulo': 'Título del Ticket',
            'descripcion_problema': 'Descripción Detallada del Problema',
            'nivel_critico': 'Nivel de Criticidad',
            'tipo_problema': 'Tipo de Problema',
        }
        # Widgets para aplicar clases de Bootstrap y mejorar la apariencia
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'nivel_critico': forms.Select(attrs={'class': 'form-select'}),
            'tipo_problema': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TicketUpdateForm(forms.ModelForm):
    """
    Formulario para que un ejecutivo actualice el estado de un ticket.
    """
    motivo_derivacion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Motivo de la Derivación o Cambio",
        required=False # No siempre es obligatorio
    )

    class Meta:
        model = Ticket
        # Añadimos 'area_asignada' a los campos editables
        fields = ['estado', 'area_asignada', 'trabajador_asignado']
        labels = {
            'estado': 'Cambiar Estado del Ticket',
            'area_asignada': 'Derivar a una Nueva Área',
            'trabajador_asignado': 'Asignar a un Nuevo Responsable'
        }
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'area_asignada': forms.Select(attrs={'class': 'form-select'}),
            'trabajador_asignado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm, self).__init__(*args, **kwargs)
        # Opcional: Limitar los trabajadores que se pueden asignar al área seleccionada.
        # Esto requeriría JavaScript en el frontend, por ahora mostramos todos.
        self.fields['trabajador_asignado'].queryset = User.objects.filter(is_active=True)

        
class ObservacionForm(forms.ModelForm):
    """
    Formulario para añadir una nueva observación a un ticket.
    """
    class Meta:
        model = Observacion
        # Solo necesitamos el campo de texto
        fields = ['observacion_texto']
        labels = {
            'observacion_texto': 'Añadir Nueva Observación'
        }
        widgets = {
            'observacion_texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe aquí una actualización o la solución aplicada...'
            })
        }