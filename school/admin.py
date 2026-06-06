from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
# Import all your models from your school/models.py
from .models import Client, Domain, AcademicClass, Subject, StudentProfile, AcademicTopic
# Import your CustomUser from your accounts app
from accounts.models import CustomUser

# 1. Register Client and Domain using TenantAdminMixin
@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on')

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')

# 2. Register your user model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'first_name', 'last_name')

# 3. Register your school core models
@admin.register(AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):
    list_display = ('level', 'stream', 'academic_year')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'lin', 'current_class')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_compulsory')

@admin.register(AcademicTopic)
class AcademicTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
