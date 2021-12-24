from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/', views.send_otp),
    path('verify-otp/', views.OTPView.as_view()),
    path('sign-up/', views.AccountCreateView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('change-password/', views.PasswordChangeView.as_view()),
]