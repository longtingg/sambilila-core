from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from accounts.models import CustomUser

# --- TENANT MODELS (Must be first for clarity) ---

class Client(TenantMixin):
    """
    Represents a school (tenant). 
    This is the master table for all your schools.
    """
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """
    Maps specific URLs/Domains to a Client.
    """
    pass

# --- SCHOOL CORE MODELS ---

class AcademicClass(models.Model):
    ZAMBIAN_LEVEL_CHOICES = [
        ('G8', 'Grade 8'), ('G9', 'Grade 9'), ('G10', 'Grade 10'), 
        ('G11', 'Grade 11'), ('G12', 'Grade 12'),
        ('F1', 'Form 1'), ('F2', 'Form 2'), ('F3', 'Form 3'), 
        ('F4', 'Form 4'), ('F5', 'Form 5'),
    ]
    level = models.CharField(max_length=3, choices=ZAMBIAN_LEVEL_CHOICES)
    stream = models.CharField(max_length=30)
    academic_year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('level', 'stream', 'academic_year')

    def __str__(self):
        return f"{self.level} - {self.stream} ({self.academic_year})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)
    is_compulsory = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'STUDENT'}, 
        related_name='student_profile'
    )
    lin = models.CharField(max_length=25, unique=True, verbose_name="Learner ID")
    current_class = models.ForeignKey(
        AcademicClass, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )
    date_of_birth = models.DateField()
    ecz_candidate_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (LIN: {self.lin})"

class AcademicTopic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
