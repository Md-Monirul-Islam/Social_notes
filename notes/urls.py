from django.urls import path # type: ignore
from .views import *

app_name = 'notes'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', userLogout, name='logout'),
    path('edit-note/', edit_note, name='edit_note'),
    path('delete-note/', delete_note, name='delete_note'),
]
