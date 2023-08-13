from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# Login required to view the home page
@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home.html', context)

# Login function (Did not use 'login' because it is already an imported function)
def login_page(request):
    # If the user is logged in they cannot access the login page
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            # Authenticating process
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, ' Username or Password is incorrect')
                
        
        context = {}
        return render(request, 'login.html', context)

# Function to log out already logged in user
def logout_user(request):
    logout(request)
    return redirect('login')

# Function to register a new user
def register(request):
    # If the user is logged in they cannot access the reister page
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account has been succesfully created for '+ user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'register.html', context)
