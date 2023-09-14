from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AvailabilityForm


@login_required
def set_availability(request):
    form = AvailabilityForm()

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            try:
                availability = form.save(commit=False)
                availability.consultant = request.user.userprofile
                availability.save()
                print("Availability data saved successfully.")
                return redirect('dashboard')
            except Exception as e:
                print(form.errors)
                print(f"Error saving availability data: {e}")
        else:
            print("Form is not valid.")
            print(form.errors)
    else:
        print("Request method is not POST.")

    return render(request, 'appointment_management/set_availability.html', {'form': form})




def dashboard(request):
    return render(request, 'appointment_management/dashboard.html')