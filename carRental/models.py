from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

TYPE_CHOICES = [('MINI', 'mini'), ('Medium', 'medium'), ('MID_RANGE', 'mid-range'), ('SEDAN', 'sedan'), ('SUV', 'suv')]
TRANSMISSION_CHOICES = [('MANUAL', 'manual'), ('AUTOMATIC', 'automatic'), ]


class RentalCompany (models.Model):
    companyName = models.CharField(max_length=100, blank=True, default='')
    companyAddress = models.CharField(max_length=100, blank=True, default='')
    companyPhoneNumber = PhoneNumberField(null=False, blank=False, unique=True)
    companyEmail = models.EmailField(max_length=254, null=False, default='')
    owner = models.ForeignKey('auth.User', related_name='carRental', on_delete=models.CASCADE, null=True)
    car = models.ForeignKey('Car', null=True, on_delete=models.CASCADE)
    companyLogo = models.ImageField(null=True)

    def __str__(self):
        return self.companyName


class Car (models.Model):
    carModel = models.CharField(max_length=100, blank=False, default='')
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, default='', max_length=100)
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, default='', max_length=100)
    carImage = models.ImageField(null=True)
    owner = models.ForeignKey('auth.User', related_name='car', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.carModel


class Manufacturer(models.Model):
    manufacturerName = models.CharField(max_length=100, blank=True, default='')
    manufacturerLogo = models.ImageField(null=True)
    owner = models.ForeignKey('auth.User', related_name='manufacturer', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.manufacturerName

