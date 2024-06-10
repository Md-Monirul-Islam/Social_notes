from django.shortcuts import render
from .forms import SignupForm

# Create your views here.
def home(request):
    return render(request,'notes/home.html')


def signup(request):
    form = SignupForm()
    data = {
        'form':form,
    }
    return render(request,'notes/signup.html',data)