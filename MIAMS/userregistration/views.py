from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import UserRegisterForm, ConsultantDetailsForm


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = form.cleaned_data['role']  # Get the selected role (group) name
            if role == 'student':
                user.groups.add(Group.objects.get(name='student'))
                return HttpResponseRedirect(reverse('student_details'))
            elif role == 'consultant':
                user.groups.add(Group.objects.get(name='consultant'))
                return HttpResponseRedirect(reverse('consultant_details'))
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

@login_required()
def student_details(request):
    # Render the student details form
    return render(request, 'users/student_details.html')

@login_required()
def consultant_details(request):
    if request.method == 'POST':
        form = ConsultantDetailsForm(request.POST)
        if form.is_valid():
            # Process the form data and save details if needed
            # Redirect to the consultant details submission page
            return redirect('home')
    else:
        form = ConsultantDetailsForm()
    return render(request, 'users/consultant_details.html', {'form': form})
def consultant_submit_details(request):
    # Handle form submission and details saving if needed
    return render(request, 'users/consultant_submit_details.html')
