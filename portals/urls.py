from django.urls import path
from . import views

urlpatterns = [
    path('school-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('educator-hub/', views.teacher_dashboard, name='teacher_dashboard'),
    path('learner-workspace/', views.student_dashboard, name='student_dashboard'),
]
