from django.db import models
from userregistration.models import UserProfile  # Import the UserProfile model

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Add any additional fields related to students here

    def __str__(self):
        return self.user_profile.user.username
