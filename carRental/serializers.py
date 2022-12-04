from rest_framework import serializers
from carRental.models import RentalCompany, Car, Manufacturer, Costumer, PlaceToStart, Rental
from django.contrib.auth.models import User


class CarRentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RentalCompany
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(many=True, queryset=Car.objects.all())
    manufacturer = serializers.PrimaryKeyRelatedField(many=True, queryset=Manufacturer.objects.all())

    class Meta:
        model = User
        fields = '__all__'


class CarSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = '__all__'


class ManufacturerSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Manufacturer
        fields = '__all__'


class CostumerSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Costumer
        fields = '__all__'


class PlaceToStartSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PlaceToStart
        fields = '__all__'


class RentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rental
        fields = '__all__'
