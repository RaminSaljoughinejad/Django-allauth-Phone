from django.urls import path
from . import views

urlpatterns = [
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path('password/otp/confirm/', views.verify_otp, name='verify-otp'),
    path('password/set/', views.set_new_password, name='set-new-password'),
]
