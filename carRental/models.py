from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class RentalCompany (models.Model):
    companyName = models.CharField(max_length=100, blank=True, default='')
    companyAddress = models.CharField(max_length=100, blank=True, default='')
    companyPhoneNumber = PhoneNumberField(null=False, blank=False, unique=True)
    companyEmail = models.EmailField(max_length=254, null=False, default='')
    owner = models.ForeignKey('auth.User', related_name='carRental', on_delete=models.CASCADE, null=True)








