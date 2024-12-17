from functools import wraps
from django.shortcuts import render

def user_required_permission(allowed_roles=None, message="Bạn không có quyền truy cập."):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            # Hiển thị thông báo quyền hạn
            return render(request, 'no_permission.html', {'message': message})
        return wrapper
    return decorator
