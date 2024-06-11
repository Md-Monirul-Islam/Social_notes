from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .forms import SignupForm

# Create your views here.
def home(request):
    return render(request,'notes/home.html')


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
        else:
            # Extract form errors and send them back in the response
            errors = form.errors.as_json()
            response = {'status': 'error', 'message': 'Invalid form submission.', 'errors': errors}
        
        return JsonResponse(response)
    
    else:
        form = SignupForm()

    return render(request, 'notes/signup.html', {'form': form})