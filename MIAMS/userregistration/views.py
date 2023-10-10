from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserProfile
from .forms import UserRegisterForm, ConsultantDetailsForm
from .forms import ConsultantDetailsForm, CertificateForm
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a UserProfile for the user
            UserProfile.objects.create(user=user)

            login(request, user)
            role = form.cleaned_data['role']
            if role == 'student':
                user.groups.add(Group.objects.get(name='student'))
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                return HttpResponseRedirect(reverse('student_details'))
            elif role == 'consultant':
                user.groups.add(Group.objects.get(name='consultant'))
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                return HttpResponseRedirect(reverse('consultant_details'))
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse('redirect_after_login')

def redirect_after_login(request):
    if request.user.groups.filter(name='consultant').exists():
        return redirect('dashboard')
    elif request.user.groups.filter(name='student').exists():
        return redirect('student_dashboard')
    else:
        # Handle other cases or roles if needed
        return redirect('home')


@login_required()
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile doesn't exist
        user_profile = None
    return render(request, 'users/profile.html', {'user_profile': user_profile})

@login_required()
def student_details(request):
    # Render the student details form
    return render(request, 'users/student_details.html')


@login_required()
def consultant_details(request):
    # Retrieve the existing UserProfile for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ConsultantDetailsForm(request.POST, request.FILES, instance=user_profile)  # Pass the existing user_profile instance

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            # Process the form data and save details if needed
            # Redirect to the consultant details submission page
            return redirect('add_certificate')
    else:
        form = ConsultantDetailsForm(instance=user_profile)  # Pass the existing user_profile instance

    return render(request, 'users/consultant_details.html', {'form': form})

def add_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user_profile = UserProfile.objects.get(user=request.user)
            certificate.save()
            return redirect('dashboard')  # Redirect back to the add_certificate page
    else:
        form = CertificateForm()

    return render(request, 'users/add_certificate.html', {'form': form})

def about_us(request):
    return  render(request, 'users/about_us.html')

def contact_us(request):
    return render(request, 'users/contact_us.html')