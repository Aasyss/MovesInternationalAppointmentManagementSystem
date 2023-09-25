from django import forms
from .models import Appointment
from userregistration.models import UserProfile
from appointment_management.models import Setup_Availability
from datetime import datetime

class AppointmentBookingForm(forms.Form):
    consultant = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    appointment_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    appointment_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    # Add any additional validation logic here if needed

    def clean(self):
        cleaned_data = super().clean()
        consultant = cleaned_data.get('consultant')
        date = cleaned_data.get('date')
        appointment_start_time = cleaned_data.get('appointment_start_time')
        appointment_end_time = cleaned_data.get('appointment_end_time')
        if consultant and date and appointment_start_time and appointment_end_time:
            day_of_week = date.weekday()
            day_of_week_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            availability = Setup_Availability.objects.get(consultant=consultant)
            available_start_time = getattr(availability, f'{day_of_week_name[day_of_week]}_start_time')
            available_end_time = getattr(availability, f'{day_of_week_name[day_of_week]}_end_time')

            selected_start_time = datetime.combine(date, appointment_start_time)
            selected_end_time = datetime.combine(date, appointment_end_time)
            if not (available_start_time <= selected_start_time.time() < available_end_time and
                    available_start_time < selected_end_time.time() <= available_end_time):
                raise forms.ValidationError("Selected time is not available.")

            if selected_end_time <= selected_start_time:
                raise forms.ValidationError("End time must be after start time.")

        return cleaned_data

