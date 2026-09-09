from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Decorator to restrict view to Admin/Warden (staff or superuser)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in as an administrator or warden to access this page.")
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access denied. Administrator privileges required.")
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """Decorator to restrict view to registered Student users."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in with your Student ID to access this page.")
            return redirect('login')
        if not hasattr(request.user, 'student_profile'):
            messages.info(request, "You are logged in as Admin. Redirected to Admin Dashboard.")
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
