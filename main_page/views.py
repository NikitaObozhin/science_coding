from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def show_page(request):
    return render(request, 'main_page/index.html')

def logout_user(request):

    logout(request)

    #messages.add_message(request, messages.SUCCESS,
                                        #'Выход выполнен успешно')

    return redirect('login/')
