from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

EDITOR_GROUP_NAME = "Editor"


def is_editor(user):
    """True if the user belongs to the 'Editor' group (managed via Django Admin)."""
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP_NAME).exists()


def can_update_data(user):
    """Editors and the owner (superuser) may update data."""
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("main.change_experience")
        or user.has_perm("main.change_project")
    )


def can_create_or_delete(user):
    """Only the portfolio owner (superuser) may create or delete data."""
    return user.is_authenticated and user.is_superuser


def permission_context(request):
    """Flags injected into every template so UI buttons can be hidden."""
    user = request.user
    return {
        "is_editor": is_editor(user),
        "can_create": can_create_or_delete(user),
        "can_update": can_update_data(user),
        "can_delete": can_create_or_delete(user),
    }


def permission_required(perm=None, superuser_only=False, login_url="/login/"):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=login_url)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if superuser_only:
                allowed = user.is_superuser
            elif perm is not None:
                allowed = user.is_superuser or user.has_perm(perm)
            else:
                allowed = True
            if not allowed:
                raise PermissionDenied  # default 403 page
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator