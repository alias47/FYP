from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import(
    UserCreationForm, UserChangeForm, PasswordChangeForm
)

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import CreateUserForm,EditProfileForm

from image.models import Photo, Category



# Create your views here.

def indexPage(request):
    
    photos = Photo.objects.filter(is_featured=True)
        
    categories = Category.objects.all()
    
    
    return render(request, 'index.html', {'photos':photos,'categories':categories})

# def indexPage(request):
#     photos = Photo.objects.all()  
#     category = request.GET.get('category')
#     if category == None:
#         photos = Photo.objects.all()
#     else:
#         photos = Photo.objects.filter(category__name=category) 
    
#     categories = Category.objects.all()
#     context = {'photos':photos, 'categories': categories}   
#     return render(request, 'index.html', context)

def searchPage(request):
    if 'q' in request.GET:
        q=request.GET['q']
        if q:
            photos = Photo.objects.filter(location__icontains=q)
    else:
        photos = Photo.objects.all()
        
    categories = Category.objects.all()
    
    
    return render(request, 'search.html', {'photos':photos,'categories':categories})
    
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
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def profilePage(request):
   
    categories = Category.objects.all()
    context = {'user': request.user, 'categories': categories}
    

    return render(request, 'profile.html', context)

     

def editProfilePage(request):
    
    categories = Category.objects.all()
    if request.method == 'POST':
        
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)
        
        context = {'form': form, 'categories': categories}
        return render(request, 'editProfile.html', context)

@login_required(login_url='login')
def changePasswordPage(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user )
            return redirect('profile')
        else:
            return redirect('change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form,'categories': categories}
        return render(request, 'password.html', context)
