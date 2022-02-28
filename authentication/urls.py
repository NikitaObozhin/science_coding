from django.urls import path

from .views import register, login_user, activate_user, verify_email

urlpatterns = [
    path('register/', register, name='register'),    
    path('login/', login_user, name='login'),
    path('activate-user/<uidb64>/<token>', activate_user, name='activate'),
    path('verify-email/', verify_email, name='verify-email')
]