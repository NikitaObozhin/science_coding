from django.shortcuts import redirect, render
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.core.cache import cache
import threading
from accessible.decorators import auth_user_should_not_access
from user_profile.models import User

from .utils import generate_token
from django.conf import settings

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def  send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Science Coding: Подтверждение E-mail'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    EmailThread(email).start()

@auth_user_should_not_access
def register(request):

    if request.method == 'POST':
        context={'has_error':False,
                'data':request.POST}
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        checked = request.POST.get('checked')
        
        if email != '':

            if not validate_email(email): 
                messages.add_message(request, messages.ERROR, 
                                        'Ошибка в E-mail адресе')
                context['has_error'] = True

            elif User.objects.filter(email=email).exists() and password != '' and password == password2:
                messages.add_message(request, messages.ERROR,
                                        'Данный E-mail уже зарегистрирован')
                context['has_error'] = True

            if len(password) < 6: 
                messages.add_message(request, messages.ERROR, 
                                        'Пароль должен быть больше 6 символов')
                context['has_error'] = True

            elif password != password2: 
                messages.add_message(request, messages.ERROR, 
                                        'Пароли должны совпадать')
                context['has_error'] = True

            if not checked and password != '' and password == password2:
                messages.add_message(request, messages.ERROR, 
                                        'Подтвердите согласие с Правилами Сайта')
                context['has_error'] = True

        else: 
            messages.add_message(request, messages.ERROR, 
                                        'Введите E-mail адрес')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        user=User.objects.create_user(username=email[:email.find('@')], email=email)
        user.set_password(password)
        user.save()

        send_activation_email(user, request)

        cache.set('email', email)
        return redirect(reverse('verify-email'))


    return render(request, 'authentication/register.html')

@auth_user_should_not_access
def login_user(request):

    if cache.get('message') != '':

        messages.add_message(request, messages.SUCCESS, 
                                cache.get('message'))
        cache.delete('message')

    if request.method == 'POST':
        context={'data':request.POST}
        email = request.POST.get('email')
        password = request.POST.get('password')

        user=authenticate(request, email=email, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 
                                    'Неверный логин или пароль')

            return render(request, 'authentication/login.html', context)

        elif not user.is_email_verified:
            send_activation_email(user, request)
            cache.set('email', email)
            return redirect(reverse('verify-email'))

        login(request, user)

        return redirect('/')

    return render(request, 'authentication/login.html')

@auth_user_should_not_access
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

    cache.set('message', 'E-mail подтвержден, вы можете войти в аккаунт')

    return redirect(reverse('login'))

@auth_user_should_not_access
def verify_email(request):

    if not cache.get('email'):
        return redirect('/')

    context = {
        'email':cache.get('email'),
        'email_servise':cache.get('email')[cache.get('email').find('@'):]
    }
    cache.delete('email')

    return render(request, 'authentication/verify-email.html', context)