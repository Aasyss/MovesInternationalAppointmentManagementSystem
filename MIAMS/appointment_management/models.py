from django.db import models
from userregistration.models import UserProfile


class Setup_Availability(models.Model):
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='consultant_availability')
    start_date = models.DateField()  # The date when availability starts
    monday_start_time = models.TimeField(null=True, blank=True)
    monday_end_time = models.TimeField(null=True, blank=True)
    tuesday_start_time = models.TimeField(null=True, blank=True)
    tuesday_end_time = models.TimeField(null=True, blank=True)
    wednesday_start_time = models.TimeField(null=True, blank=True)
    wednesday_end_time = models.TimeField(null=True, blank=True)
    thursday_start_time = models.TimeField(null=True, blank=True)
    thursday_end_time = models.TimeField(null=True, blank=True)
    friday_start_time = models.TimeField(null=True, blank=True)
    friday_end_time = models.TimeField(null=True, blank=True)
    saturday_start_time = models.TimeField(null=True, blank=True)
    saturday_end_time = models.TimeField(null=True, blank=True)
    sunday_start_time = models.TimeField(null=True, blank=True)
    sunday_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Availability for {self.consultant.user.username} starting on {self.start_date}"


class Appointment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student_appointments')
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='consultant_appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.student.user.username} - {self.consultant.user.username} - {self.date} {self.start_time} - {self.end_time}"