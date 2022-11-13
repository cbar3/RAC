from rest_framework import serializers
from carRental.models import RentalCompany, Car, Manufacturer, Costumer, PlaceToStart, Rental
from django.contrib.auth.models import User


class CarRentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RentalCompany
        fields = ['id', 'companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail', 'owner', 'car',
                  'companyLogo', 'costumer', 'placeToStart']


class UserSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(many=True, queryset=Car.objects.all())
    manufacturer = serializers.PrimaryKeyRelatedField(many=True, queryset=Manufacturer.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'car', 'manufacturer']


class CarSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ['id', 'carModel', 'manufacturer', 'type', 'transmission', 'carImage', 'owner']


class ManufacturerSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ['id', 'manufacturer', 'manufacturerLogo', 'owner']


class CostumerSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Costumer
        fields = ['id', 'costumerFirstName', 'costumerLastName', 'costumerEmail', 'costumerPhoneNumber',
                  'costumerAFM', 'owner']


class PlaceToStartSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PlaceToStart
        fields = ['id', 'placeToStart', 'owner']


class RentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rental
        fields = ['id', 'costumer', 'rentalCompany', 'car', 'startDate', 'finishDate', 'placeToStart',
                  'owner']
