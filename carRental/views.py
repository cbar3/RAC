from carRental.models import RentalCompany, Car, Manufacturer, Rental, Costumer, PlaceToStart
from carRental.serializers import CarRentalSerializer, CarSerializer, ManufacturerSerializer, RentalSerializer, \
    CostumerSerializer, PlaceToStartSerializer
from carRental.serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from carRental.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarCompanyList(generics.ListCreateAPIView):
    """
    Returns a List of all companies
    """
    queryset = RentalCompany.objects.all()
    serializer_class = CarRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ('companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail')
    search_fields = ('companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarCompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentalCompany.objects.all()
    serializer_class = CarRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CarList (generics.ListCreateAPIView):
    """
    Returns a List of all cars
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ('carModel', 'manufacturer', 'type')
    search_fields = ('carModel', 'manufacturer', 'type')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ManufacturerList (generics.ListCreateAPIView):

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('manufacturerName',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ManufacturerDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CustomerList (generics.ListCreateAPIView):

    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('costumerFirstName', 'costumerLastName', 'costumerEmail', 'costumerPhoneNumber',
                     'costumerAFM')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CustomerDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('costumer', 'rentalCompany', 'car', 'startDate', 'finishDate'
                     'placeToStart')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RentalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PlaceToStartList(generics.ListCreateAPIView):
    queryset = PlaceToStart.objects.all()
    serializer_class = PlaceToStartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('placeToStart',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceToStartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaceToStart.objects.all()
    serializer_class = PlaceToStartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
