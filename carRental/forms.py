from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from carRental.models import Car, Costumer, RentalCompany


class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    AFM = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User, Costumer
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'AFM']


