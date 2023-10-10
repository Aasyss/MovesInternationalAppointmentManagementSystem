from django.db import models
from userregistration.models import UserProfile
from book_appointment.models import Appointment

class Payment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_payments')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Payment for {self.appointment}"

    def mark_as_paid(self):
        self.payment_status = 'paid'
        self.save()

    def mark_as_pending(self):
        self.payment_status = 'pending'
        self.save()
