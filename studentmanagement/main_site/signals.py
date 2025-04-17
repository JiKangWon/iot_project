from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Class_Student)
def create_attendance_records(sender, instance, created, **kwargs):
    if created:  # Only run when the Class_Student is created, not updated
        for session in range(1, instance.class_obj.sessions_number + 1):
            Attendance.objects.create(
                class_student=instance,
                session_order=session,
                status='absent'  # Default status as per your model
            )

@receiver(post_save, sender=Class)
def create_attendance_date(sender, instance, created, **kwargs):
    if created:
        for session in range(1, instance.sessions_number + 1):
            Attendance_Date.objects.create(
                class_obj=instance,
                date=instance.start_day + timedelta(weeks=session-1),
                session_order=session
            )