from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def login_user(request):

    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        print('wtf')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('cabinet')

        else:
            messages.success(request, ("Упс, что-то пошло не так :("))
            return redirect('login')

    else:
        return render(request, 'authentication/login.html', {})


def logout_user(request):

    logout(request)
    return redirect('login')