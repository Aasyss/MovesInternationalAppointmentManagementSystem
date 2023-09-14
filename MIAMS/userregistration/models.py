from django.contrib.auth.models import User, Group
from django.db import models

# Define the user groups
GROUPS = (
    ('student', 'Student'),
    ('consultant', 'Consultant'),
)

# Define expertise choices
EXPERTISE_CHOICES = [
    ('Visa Counselor', 'Visa Counselor'),
    ('Career Counselor', 'Career Counselor'),
    ('Migration Counselor', 'Migration Counselor'),
    ('Stress Counselor', 'Stress Counselor'),
]

# Create the groups in the database if they don't exist
for group_name, group_label in GROUPS:
    Group.objects.get_or_create(name=group_name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    education_history = models.TextField(null=True, blank=True)
    expertise = models.CharField(
        max_length=50,
        choices=EXPERTISE_CHOICES,
        blank=True,
        null=True
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Certificate(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')
