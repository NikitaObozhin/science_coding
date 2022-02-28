from django.urls import path

from .views import show_page, logout_user

urlpatterns = [
    path('', show_page),    
    path('logout_user', logout_user, name='logout_user'),
]