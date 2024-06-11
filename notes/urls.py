from django.urls import path
from .views import *

app_name = 'notes'

urlpatterns = [
    path('',home,name='home'),
    path('signup/',signup,name='signup'),
]