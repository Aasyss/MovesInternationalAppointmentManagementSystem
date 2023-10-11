from django.urls import path
from .views import checkout,  create_checkout_session, stripe_config
from . import views
app_name = 'payment'

urlpatterns = [
    path('config/', stripe_config),  # new
    path('checkout/<int:appointment_id>/', checkout, name='checkout'),
    path('success/', views.SuccessView.as_view()),  # new
    path('create-checkout-session/<int:appointment_id>/', create_checkout_session),
    ]