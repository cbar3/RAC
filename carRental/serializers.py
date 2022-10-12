from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from carRental.models import RentalCompany
from django.contrib.auth.models import User


class CarRentalSerializer (serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RentalCompany
        fields = ['id', 'companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail', 'owner']


class UserSerializer(serializers.ModelSerializer):
    companyNames = serializers.PrimaryKeyRelatedField(many=True, queryset=RentalCompany.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'companyNames']







