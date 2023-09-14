# student/views.py

from django.shortcuts import render
from userregistration.models import UserProfile  # Import the UserProfile model
from appointment_management.models import Setup_Availability  # Import the Setup_Availability model


def student_dashboard(request):
    selected_expertise = request.GET.get('expertise')

    if selected_expertise:
        consultants = UserProfile.objects.filter(expertise=selected_expertise)
    else:
        consultants = UserProfile.objects.filter(user__groups__name='consultant')

    return render(request, 'student/student_dashboard.html', {'consultants': consultants, 'selected_expertise': selected_expertise})

# def student_dashboard(request):
#     consultants = UserProfile.objects.filter(user__groups__name='consultant')
#     selected_expertise = request.GET.get('expertise')
#     return render(request, 'student/student_dashboard.html', {'consultants': consultants, 'selected_expertise': selected_expertise})



def view_consultant_details(request, user_profile_id):
    consultant = UserProfile.objects.get(id=user_profile_id)
    availabilities = Setup_Availability.objects.filter(consultant=consultant)
    return render(request, 'student/view_consultant_details.html', {'consultant': consultant, 'availabilities': availabilities})
