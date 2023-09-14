from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from .views import CustomLoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('redirect_after_login/', views.redirect_after_login, name='redirect_after_login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('student-details/', views.student_details, name='student_details'),
    path('consultant-details/', views.consultant_details, name='consultant_details'),
    path('add_certificate/', views.add_certificate, name='add_certificate'),
    path('about_us/', views.about_us, name='about_us'),

]
