from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Format: +260...")

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
