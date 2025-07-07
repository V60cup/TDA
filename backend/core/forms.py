# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Area

class RegistroUsuarioForm(UserCreationForm):
    # Añadimos los campos del Perfil al formulario
    rol = forms.ChoiceField(choices=Perfil.Roles.choices, required=True)
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

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