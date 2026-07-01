from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def job_seeker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'profile') and request.user.profile.role == 'job_seeker':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. This page is only for Job Seekers.")
        return redirect('home')

    return wrapper


def company_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'company_admin':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. This page is only for Company Admins.")
        return redirect('home')

    return wrapper
