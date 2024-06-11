from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from .forms import SignupForm,LoginForm

def home(request):
    return render(request, 'notes/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(
                first_name=name,
                username=username,
                email=email,
                password=password
            )
            response = {'status': 'success', 'message': 'User registered successfully.'}
            return JsonResponse(response)
        else:
            errors = form.errors.as_json()
            response = {'status': 'error', 'message': 'Invalid form submission.', 'errors': errors}
            return JsonResponse(response)
    else:
        form = SignupForm()

    return render(request, 'notes/signup.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('notes:login')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    data = {
        'form': form,
    }

    return render(request, 'notes/login.html', data)
