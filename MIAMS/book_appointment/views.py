from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentBookingForm
from .models import Appointment
from appointment_management.models import Setup_Availability
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def book_appointment(request):
    day_of_week_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            consultant = form.cleaned_data['consultant']
            date = form.cleaned_data['date']
            appointment_start_time = form.cleaned_data['appointment_start_time']
            appointment_end_time = form.cleaned_data['appointment_end_time']
            print(request.user.username)
            # Check if the selected time slot is available
            availability = Setup_Availability.objects.get(consultant=consultant)
            day_of_week = date.weekday()
            available_start_time = getattr(availability, f'{day_of_week_name[day_of_week]}_start_time')
            available_end_time = getattr(availability, f'{day_of_week_name[day_of_week]}_end_time')

            selected_start_time = datetime.combine(date, appointment_start_time)
            selected_end_time = datetime.combine(date, appointment_end_time)

            if (available_start_time <= selected_start_time.time() < available_end_time and
                    available_start_time < selected_end_time.time() <= available_end_time):
                student_email = request.user.email
                consultant_email = consultant.user.email
                print(student_email)
                # The selected time slot is available, so create the appointment
                appointment = Appointment(
                    student=request.user.userprofile,
                    consultant=consultant,
                    appointment_datetime=selected_start_time,
                    appointment_start_time=selected_start_time,
                    appointment_end_time=selected_end_time,
                )
                appointment.save()
                send_appointment_confirmation_email(
                    student_email, consultant_email, date,
                    appointment_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    appointment_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    student_name=f"{request.user.first_name} {request.user.last_name}",
                    consultant_name=f"{consultant.user.first_name} {consultant.user.last_name}"
                )

                # Set the availability slot as unavailable
                setattr(availability, f'{day_of_week_name[day_of_week]}_start_time', selected_end_time.time())
                availability.save()

                return redirect('appointment_success')
    else:
        form = AppointmentBookingForm()

    return render(request, 'book_appointment/book_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'book_appointment/appointment_success.html')


def send_appointment_confirmation_email(student_email, consultant_email, date, start_time, end_time, student_name, consultant_name):
    # Render the HTML templates for the email content
    print(student_name)
    print(consultant_name)
    student_message = render_to_string('email/appointment_booked_student.html', {
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'consultant_name': consultant_name,
        'student_name':student_name
    })

    consultant_message = render_to_string('email/appointment_booked_consultant.html', {
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'student_name': student_name,
        'consultant_name':consultant_name
    })

    # Send email to student
    send_mail(
        'Appointment Booked',
        student_message,
        'movesinternationaldemoproject@gmail.com',
        [student_email],
        fail_silently=False,
        html_message=student_message
    )

    # Send email to consultant
    send_mail(
        'Appointment Booked',
        consultant_message,
        'movesinternationaldemoproject@gmail.com',
        [consultant_email],
        fail_silently=False,
        html_message=consultant_message
    )