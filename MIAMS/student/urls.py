from django.urls import path
from . import views

urlpatterns = [
    # Add other URL patterns if any
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('consultant/<int:user_profile_id>/', views.view_consultant_details, name='view_consultant_details'),]
