from django.db import models
from userregistration.models import UserProfile
from appointment_management.models import Appointment

class Notification(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    notification_time = models.DateTimeField()

    def __str__(self):
        return f"Notification for {self.student.user.username} - {self.consultant.user.username} - {self.appointment.appointment_datetime}"
