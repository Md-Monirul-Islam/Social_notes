from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from django.contrib.auth import authenticate, login as auth_login,logout # type: ignore
from django.http import JsonResponse # type: ignore
from .forms import SignupForm,LoginForm,NoteForm
from .models import Note

def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user = request.user).order_by('-id')
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            print(title,'----',description)
            note = Note()
            note.title = title
            note.description = description
            note.user = request.user
            note.save()

            notes = Note.objects.values().filter(user = request.user).order_by('-id')
            note_list = list(notes)
            response = {
                'status': 'Note added successfully!',
                'note_list':note_list
                }
            return JsonResponse(response)
        form = NoteForm()
        data = {
            'form':form,
            'notes':notes,
        }
        return render(request, 'notes/home.html',data)
    else:
        return redirect('notes:login')
    

def edit_note(request):
    edit_id = request.POST.get('edit_id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    Note.objects.filter(id=edit_id).update(title=title, description=description)
    
    # Retrieve the updated note
    updated_note = Note.objects.values().get(id=edit_id)
    
    response = {
        'status': 'Note Updated successfully!',
        'updated_note': updated_note
    }
    return JsonResponse(response)



def delete_note(request):
    delete_id = request.GET.get('delete_id')
    note = Note.objects.filter(id=delete_id).first()
    
    if note:
        note.delete()
        status_message = 'Note deleted successfully!'
    else:
        status_message = 'Note not found!'
    
    notes = Note.objects.filter(user=request.user).order_by('-id')
    note_list = list(notes.values('id', 'title', 'description'))
    
    response = {
        'status': status_message,
        'note_list': note_list
    }
    
    return JsonResponse(response)


    
    

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
            
            try:
                user = authenticate(request, username=username, password=password)
                print(username,password)
            except:
                return JsonResponse({'status':'Invalid username or password.'})
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'status':"User login successfully"})
                # messages.success(request,"User login successfull.")
                # return redirect('notes:login') # redirect using ajax
            else:
                # messages.error(request, 'Invalid username or password.')
                return JsonResponse({'status':'Invalid username or password.'})
        else:
            return JsonResponse({'status':'Invalid username or password.'})
    else:
        form = LoginForm()
    
    data = {
        'form': form,
    }

    return render(request, 'notes/login.html', data)


def userLogout(request):
    logout(request)
    return redirect('notes:login')
