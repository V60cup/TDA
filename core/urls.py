from django.urls import path
from .views import home_view # ¡Asegúrate de que la importación es correcta!

urlpatterns = [
    # La ruta ('') debe ser una cadena de texto.
    # home_view debe ser la función que importaste.
    path('', home_view, name='home'),
]