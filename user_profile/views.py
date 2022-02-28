from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from authentication.views import send_activation_email
from django.contrib.auth.decorators import login_required
from validate_email import validate_email
from django.contrib import messages
from django.core.cache import cache

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    if user != request.user:
        return redirect(f'/profile/{ request.user.username }/')

    if request.method == 'POST':

        if '_save' in request.POST: 

            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.sex = request.POST.get('sex')
            user.bio = request.POST.get('bio')

            try:
                if request.FILES['avatar']:
                    file = request.FILES['avatar']
                    fs = FileSystemStorage(location=f'media/user_{user.pk}/')
                    fs.save(file.name, file)
                    user.user_avatar = f'user_{user.pk}/' + file.name
            except: pass

        elif '_delete' in request.POST:
             user.user_avatar = 'default_avatar.png'
     
        user.save()

    user = get_object_or_404(User, username=username)


    return render(request, 'user_profile/user_profile.html', {'user' : user})

@login_required
def user_security(request, username):
    user = get_object_or_404(User, username=username)
    context={'has_error':False,
                'data':request.POST}

    if user != request.user:
        return redirect(f'/security/{ request.user.username }/')

    if request.method == 'POST':
        if '_save_email' in request.POST: 
            email = request.POST.get('email')
            if not validate_email(email): 
                messages.add_message(request, messages.ERROR, 
                                        'Ошибка в формате E-mail адреса')
                context['has_error'] = True
                return render(request, 'user_profile/user_security.html', context)
            if user.email != email:
                user.email = email
                user.is_email_verified = False
                user.save()
                if not user.is_email_verified:
                    send_activation_email(user, request)
                    context = {
                    'email':email,
                    'email_servise':email[email.find('@'):]
                    }

                    return render(request, 'authentication/verify-email.html', context)
        if '_save_password' in request.POST: 
            password = request.POST.get('password')
            if len(password) < 6:
                messages.add_message(request, messages.ERROR, 
                                        'Пароль должен быть больше 6 символов')
                context['has_error'] = True
                return render(request, 'user_profile/user_security.html', context)
            user.set_password(password)
            user.save()
            cache.set('message', 'Пароль был успешно изменен, выполните вход в аккаунт')
            return redirect('/login/')
                
    return render(request, 'user_profile/user_security.html', {'user' : user})
