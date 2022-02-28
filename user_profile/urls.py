from django.urls import path

from .views import *

urlpatterns = [
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('security/<str:username>/', user_security, name='user_security')
]