from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('portal_redirect')
    return render(request, 'home.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('portal_redirect')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('portal_redirect')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html')

def portal_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if user.is_superuser:
        return redirect('/system-master-panel/')
    
    role_redirects = {
        'ADMIN': 'admin_dashboard',
        'TEACHER': 'teacher_dashboard',
        'STUDENT': 'student_dashboard',
        'PARENT': 'parent_dashboard',
    }
    
    return redirect(role_redirects.get(user.role, 'home'))
