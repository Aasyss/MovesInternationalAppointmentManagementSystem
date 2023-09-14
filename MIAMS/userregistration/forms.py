from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile, Certificate

STATES = (
    ('', 'Choose...'),
    ('NSW', 'New South Wales'),
    ('QLD', 'Queensland'),
    ('SA', 'South Australia'),
    ('NT', 'Northern Territory'),
    ('Tas', 'Tasmania'),
    ('Vic', 'Victoria'),
    ('WA', 'Western Australia')
)


ROLE_CHOICES = (
    ('student', 'Student'),
    ('consultant', 'Consultant'),
)



class UserRegisterForm(UserCreationForm):
    # Add a hidden field to store the consultant's ID

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'username',
            'placeholder': ('Username')
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'first_name',
            'placeholder': ('First Name')
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'last_name',
            'placeholder': ('Last Name')
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'type': 'email',
            'placeholder': ('Email')
        }
    ))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
            'placeholder': 'Repeat Password'
        }
    ))

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2','role', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'check_me_out']


class ConsultantDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'cv', 'date_of_birth', 'education_history', 'expertise']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_file']

