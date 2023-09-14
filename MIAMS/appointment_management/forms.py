from django import forms
from django.utils import timezone
from .models import UserProfile
from.models import Setup_Availability


class AppointmentBookingForm(forms.Form):
    consultant = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user__groups__name='consultant'))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Setup_Availability
        fields = [
            'start_date',
            'monday_start_time', 'monday_end_time',
            'tuesday_start_time', 'tuesday_end_time',
            'wednesday_start_time', 'wednesday_end_time',
            'thursday_start_time', 'thursday_end_time',
            'friday_start_time', 'friday_end_time',
            'saturday_start_time', 'saturday_end_time',
            'sunday_start_time', 'sunday_end_time'
        ]
