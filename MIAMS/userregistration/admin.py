from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture', 'bio', 'cv', 'date_of_birth', 'education_history', 'is_verified']

admin.site.register(UserProfile, UserProfileAdmin)