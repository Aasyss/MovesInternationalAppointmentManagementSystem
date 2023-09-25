from django.shortcuts import render, redirect
from .forms import AppointmentBookingForm
from .models import Appointment
from appointment_management.models import Setup_Availability
from datetime import datetime

def book_appointment(request):
    day_of_week_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            consultant = form.cleaned_data['consultant']
            date = form.cleaned_data['date']
            appointment_start_time = form.cleaned_data['appointment_start_time']
            appointment_end_time = form.cleaned_data['appointment_end_time']

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

                # Set the availability slot as unavailable
                setattr(availability, f'{day_of_week_name[day_of_week]}_start_time', selected_end_time.time())
                availability.save()

                return redirect('appointment_success')
    else:
        form = AppointmentBookingForm()

    return render(request, 'book_appointment/book_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'book_appointment/appointment_success.html')
