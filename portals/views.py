from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from school.models import Subject, AcademicTopic, CustomUser
from django.contrib import messages

# Note: Ensure you have your custom decorators defined in accounts.decorators 
# that check user.role == 'ADMIN', etc.

@login_required
def admin_dashboard(request):
    # Check if the user is an admin
    if request.user.role != 'ADMIN':
        return redirect('home')

    teachers = CustomUser.objects.filter(role='TEACHER')
    students = CustomUser.objects.filter(role='STUDENT')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if username and password:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, f"User ID '{username}' already exists.")
            else:
                role = 'TEACHER' if action == 'add_teacher' else 'STUDENT'
                new_user = CustomUser.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name,
                    role=role
                )
                messages.success(request, f"Profile provisioned for {first_name}.")
                return redirect('admin_dashboard')

    context = {'teachers': teachers, 'students': students}
    return render(request, 'portals/admin_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return redirect('home')

    subjects = Subject.objects.all()
    topics = AcademicTopic.objects.all()
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_select')
        title = request.POST.get('title')
        
        if subject_id and title:
            target_sub = Subject.objects.get(id=subject_id)
            AcademicTopic.objects.create(subject=target_sub, title=title)
            messages.success(request, "Syllabus entry successfully synchronized.")
            return redirect('teacher_dashboard')

    context = {'subjects': subjects, 'topics': topics}
    return render(request, 'portals/teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    lessons = AcademicTopic.objects.select_related('subject').all()
    context = {'lessons': lessons}
    return render(request, 'portals/student_dashboard.html', context)
