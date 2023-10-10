from django.db import models
from userregistration.models import UserProfile

class Appointment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student_appointments')
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='consultant_appointments')
    appointment_datetime = models.DateTimeField()
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.consultant.user.username} - {self.appointment_datetime}"