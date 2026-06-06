from django.core.exceptions import PermissionDenied

def school_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_school_admin:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper
