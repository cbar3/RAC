from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from carRental.models import RentalCompany, Car, Manufacturer
from django.contrib.auth.models import User


class CarRentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RentalCompany
        fields = ['id', 'companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail', 'owner', 'car',
                  'companyLogo']


class UserSerializer(serializers.ModelSerializer):
    companyNames = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalCompany.objects.all())
    car = serializers.PrimaryKeyRelatedField(many=True, queryset=Car.objects.all())
    manufacturer = serializers.PrimaryKeyRelatedField(many=True, queryset=Manufacturer.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'companyNames', 'car']


class CarSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ['id', 'carModel', 'manufacturer', 'type', 'transmission', 'carImage', 'owner']


class ManufacturerSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ['id', 'manufacturerName', 'manufacturerLogo', 'owner']




