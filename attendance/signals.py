from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AttendanceRecord
from core.sms_service import send_parent_sms

@receiver(post_save, sender=AttendanceRecord)
def trigger_absentee_alert(sender, instance, created, **kwargs):
    """
    Listens for saved attendance records. If a student is marked Absent (Unexcused),
    it immediately alerts the parent.
    """
    if instance.status == 'ABSENT' and not instance.sms_alert_sent:
        
        # Look up the parent's number (assuming you added emergency_contact to StudentProfile)
        parent_number = instance.student.emergency_contact_number 
        student_name = instance.student.user.get_full_name()
        date_str = instance.date.strftime("%d %b %Y")
        
        message = (
            f"Notice from Sambilila Core: {student_name} was marked absent "
            f"from school today ({date_str}) without prior excuse. "
            f"Please contact the administration office for clarification."
        )
        
        # Trigger the SMS API
        success = send_parent_sms(parent_number, message)
        
        # If the API accepted the message, mark it as sent so we don't duplicate
        if success:
            # We use QuerySet update to avoid re-triggering the post_save signal infinitely
            AttendanceRecord.objects.filter(id=instance.id).update(sms_alert_sent=True)
