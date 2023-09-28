from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from notifications.models import Notification
from appointment_management.models import Appointment

class Command(BaseCommand):
    help = 'Send notifications for upcoming appointments'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        twelve_hours_later = now + timedelta(hours=12)
        upcoming_appointments = Appointment.objects.filter(appointment_datetime__gte=now, appointment_datetime__lte=twelve_hours_later)

        for appointment in upcoming_appointments:
            student = appointment.student
            consultant = appointment.consultant

            notification_time = appointment.appointment_datetime - timedelta(hours=12)

            # Create a notification for the student
            student_notification = Notification(
                student=student,
                consultant=consultant,
                appointment=appointment,
                notification_time=notification_time
            )
            student_notification.save()

            # Create a notification for the consultant
            consultant_notification = Notification(
                student=student,
                consultant=consultant,
                appointment=appointment,
                notification_time=notification_time
            )
            consultant_notification.save()

            # Send email notification to student
            student_subject = f'Appointment Reminder'
            student_message = render_to_string('notifications/appointment_reminder.html', {
                'name': student.user.first_name,
                'appointment_time': appointment.appointment_datetime,
            })
            send_mail(student_subject, student_message, 'movesinternationaldemoproject@gmail.com', [student.user.email], html_message=student_message)

            # Send email notification to consultant
            consultant_subject = f'Appointment Reminder'
            consultant_message = render_to_string('notifications/appointment_reminder.html', {
                'name': consultant.user.first_name,
                'appointment_time': appointment.appointment_datetime,
            })
            send_mail(consultant_subject, consultant_message, 'movesinternationaldemoproject@gmail.com', [consultant.user.email],
                      html_message=consultant_message)
