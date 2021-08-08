from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterView, VerifyEmail, LoginAPIView

app_name='users'

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('email_verify/',VerifyEmail.as_view(), name='email_verify'),
    path('login/', LoginAPIView.as_view(),name='login'),
]