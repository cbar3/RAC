from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from carRental.models import Car, Costumer, RentalCompany, Manufacturer


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'inpBoxCustomer'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'inpBoxCustomer'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inpBoxCustomer'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inpBoxCustomer'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'inpBoxCustomer'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'inpBoxCustomer'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'inpBoxCustomer'}), required=False)
    AFM = forms.CharField(widget=forms.NumberInput(attrs={'class': 'inpBoxCustomer'}), required=False)

    class Meta:
        model = User, Costumer
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'AFM']


class CustomerUpdate(forms.ModelForm):
    class Meta:
        model = Costumer
        fields = ['profilePic', 'costumerFirstName', 'costumerLastName', 'costumerEmail', 'costumerPhoneNumber']
        widgets = {
            'costumerEmail': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'costumerFirstName': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'costumerLastName': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'costumerPhoneNumber': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
        }


class ProductUpdate(forms.ModelForm):
    TYPE_CHOICES = [('MINI', 'mini'), ('Medium', 'medium'), ('MID_RANGE', 'mid-range'), ('SEDAN', 'sedan'),
                    ('SUV', 'suv')]
    TRANSMISSION_CHOICES = [('MANUAL', 'manual'), ('AUTOMATIC', 'automatic')]

    transmission = forms.ChoiceField(choices=TRANSMISSION_CHOICES),
    type = forms.ChoiceField(choices=TYPE_CHOICES),

    class Meta:
        model = Car
        fields = ['carModel', 'type', 'transmission', 'carImage', 'price', 'insurance', 'tank']
        widgets = {
            'carModel': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'price': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'insurance': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
            'tank': forms.TextInput(attrs={'class': 'inpBoxCustomer'}),
        }


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['carModel', 'manufacturer', 'type', 'transmission', 'carImage', 'price', 'insurance', 'tank']
        widget = {
            'carModel': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.IntegerField(),
            'tank': forms.IntegerField(),
            'transmission': forms.ModelMultipleChoiceField(queryset=Car.objects.all()),
            'type': forms.ModelMultipleChoiceField(queryset=Car.objects.all()),
            'manufacturer': forms.ModelMultipleChoiceField(queryset=Manufacturer.objects.all()),
        }


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'inpBoxCustomer'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inpBoxCustomer'}))

    class Meta:
        model = User
        fields = ['username', 'password']

