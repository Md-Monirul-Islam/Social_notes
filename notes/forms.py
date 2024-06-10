from django import forms

class SignupForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    username = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField()
    confirm_password = forms.CharField()