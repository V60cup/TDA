# core/decorators.py
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            # Asumimos que el usuario está logueado y tiene un perfil
            if hasattr(request.user, 'perfil') and request.user.perfil.rol in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Si no tiene el rol, se le niega el acceso
                raise PermissionDenied
        return wrap
    return decorator