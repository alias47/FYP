from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import CreateUserForm

# Create your views here.


def indexPage(request):
    return render(request, 'index.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def profilePage(request):
    context = {'user': request.user}

    return render(request, 'profile.html', context)


def editProfilePage(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = UserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'editProfile.html', context)
