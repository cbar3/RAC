from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField, PhoneNumber

TYPE_CHOICES = [('MINI', 'mini'), ('Medium', 'medium'), ('MID_RANGE', 'mid-range'), ('SEDAN', 'sedan'), ('SUV', 'suv')]
TRANSMISSION_CHOICES = [('MANUAL', 'manual'), ('AUTOMATIC', 'automatic')]
PLACE_CHOICES = [('Home', 'home'), ('Airport', 'airport'), ('KTEL', 'ktel')]


class RentalCompany (models.Model):
    companyName = models.CharField(max_length=100, blank=True, default='')
    companyAddress = models.CharField(max_length=100, blank=True, default='')
    companyPhoneNumber = PhoneNumberField(null=False, blank=False, unique=True)
    companyEmail = models.EmailField(max_length=254, null=False, default='')
    owner = models.ForeignKey('auth.User', related_name='carRental', on_delete=models.CASCADE, null=True)
    costumer = models.ManyToManyField('Costumer')
    car = models.ManyToManyField('Car')
    placeToStart = models.ManyToManyField('PlaceToStart')
    companyLogo = models.ImageField(null=True)

    def __str__(self):
        return self.companyName


class Costumer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    costumerFirstName = models.CharField(max_length=80, null=False, default='')
    costumerLastName = models.CharField(max_length=80, null=False, default='')
    costumerEmail = models.EmailField(max_length=254, null=False, default='')
    costumerPhoneNumber = PhoneNumberField(null=False, blank=False, unique=True)
    costumerAFM = models.IntegerField(null=False, default='')

    def __str__(self):
        return self.costumerFirstName


class Car (models.Model):
    carModel = models.CharField(max_length=100, blank=False, default='')
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, default='', max_length=15)
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, default='', max_length=15)
    carImage = models.ImageField(null=True)
    owner = models.ForeignKey('auth.User', related_name='car', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.carModel


class PlaceToStart(models.Model):
    placeToStart = models.CharField(max_length=15, choices=PLACE_CHOICES)

    def __str__(self):
        return self.placeToStart


class Manufacturer(models.Model):
    manufacturerName = models.CharField(max_length=100, blank=True, default='')
    manufacturerLogo = models.ImageField(null=True)
    owner = models.ForeignKey('auth.User', related_name='manufacturer', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.manufacturerName


class Rental(models.Model):
    costumer = models.ForeignKey('Costumer', null=True, on_delete=models.CASCADE)
    rentalCompany = models.ForeignKey('RentalCompany', null=True, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', null=True, on_delete=models.CASCADE)
    startDate = models.DateField()
    finishDate = models.DateField()
    placeToStart = models.ForeignKey('PlaceToStart', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.costumer
