from django.db import models
from django.utils import timezone
# FIX: Corrected import path to reference the 'school' app
from school.models import StudentProfile, AcademicClass

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent (Unexcused)'),
        ('EXCUSED', 'Absent (Excused/Sick)'),
        ('LATE', 'Late'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    
    # Critical for SMS logic
    sms_alert_sent = models.BooleanField(
        default=False, 
        help_text="Tracks whether the automated SMS has already been dispatched for this absence."
    )
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # A student can only have one primary attendance record per day
        unique_together = ('student', 'date')

    def __str__(self):
        # We access student.user.get_full_name() because the relationship is established
        return f"{self.student.user.get_full_name()} - {self.date} ({self.get_status_display()})"
