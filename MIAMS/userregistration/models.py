from django.contrib.auth.models import User, Group
from django.db import models

# Define the user groups
GROUPS = (
    ('student', 'Student'),
    ('consultant', 'Consultant'),
)

# Create the groups in the database if they don't exist
for group_name, group_label in GROUPS:
    Group.objects.get_or_create(name=group_name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
