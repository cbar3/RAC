from django.contrib.auth import authenticate, login, logout
from carRental.models import RentalCompany, Car, Manufacturer, Rental, Costumer, PlaceToStart, Extras
from carRental.serializers import CarRentalSerializer, CarSerializer, ManufacturerSerializer, RentalSerializer, \
    CostumerSerializer, PlaceToStartSerializer
from carRental.serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from carRental.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, timedelta, date
from json import dumps


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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('Name', 'Address', 'Phone Number', 'Email')
    search_fields = ('companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail')
    ordering_fields = ('companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarCompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentalCompany.objects.all()
    serializer_class = CarRentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CarList(generics.ListCreateAPIView):
    """
    Returns a List of all cars
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ('carModel', 'manufacturer', 'type')
    search_fields = ('carModel', 'manufacturer', 'type')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ('manufacturerName',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CustomerList(generics.ListCreateAPIView):
    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ('costumerFirstName', 'costumerLastName', 'costumerEmail', 'costumerPhoneNumber',
                     'costumerAFM')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ('placeToStart',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceToStartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaceToStart.objects.all()
    serializer_class = PlaceToStartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


def home(request):
    cars = Car.objects.all().order_by('carModel')[:12]
    return render(request, 'home.html', {'cars': cars})


def carlist(request):
    cars = Car.objects.all().order_by('carModel')
    return render(request, 'carlist.html', {'cars': cars})


def cardetail(request, pk):
    cars = get_object_or_404(Car, pk=pk)
    carRelated = Car.objects.all().order_by('carModel')[:4]
    if request.method == 'POST':
        message_name = request.POST['name'] + ' ' + " " + request.POST['number']
        message_email = request.POST['email']
        message = request.POST['message']
        send_mail(
            message_name,
            message,
            message_email,
            ['c.barbas@oustrias.gr'],
            fail_silently=False
        )

    context = {'cars': cars,
               'carRelated': carRelated}
    return render(request, 'cardetails.html', context)


def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'home.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html')


def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.afm = form.cleaned_data['AFM']
                user.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return HttpResponseRedirect('account')

    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


@login_required(login_url='home.html')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home.html')
def createRental(request, pk):
    dataHolder = []
    dataClean = []
    current = request.user
    carData = Car.objects.get(id=pk)
    pickupPlace = PlaceToStart.objects.all()
    rawData = Rental.objects.filter(carId=pk)
    priceOfAddi = Extras.objects.last()

    # making a list of blocked days for date picker
    for x in rawData:
        if x.finishDate > datetime.now().date():
            srtDate = x.startDate
            endDate = x.finishDate
            delta = endDate - srtDate
            dataHolder = [(srtDate + timedelta(days=i)) for i in range(delta.days + 1)]

    dataClean = [x.strftime("%m/%d/%Y") for x in dataHolder]
    dataClean = dumps(dataClean)

    context = {
        'current': current,
        'carData': carData,
        'dataClean': dataClean,
        'pickupPlace': pickupPlace,
        'priceOfAddi': priceOfAddi
    }
    return render(request, 'rental.html', context, )


@login_required(login_url='home.html')
def order(request, pk):
    car = Car.objects.get(id=pk)
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    current = request.user

    format = "%Y/%m/%d"
    if (request.method == 'POST' and endDate > startDate):
        additions = 0
        priceOfAddi = Additions.objects.last()
        sdate = datetime.strptime(startDate, format)
        edate = datetime.strptime(endDate, format)
        daysTotal = edate - sdate
        days = int(daysTotal.days)
        place = Location.objects.get(id=request.POST['pickUpPlace'])
        fuel = request.POST.get('fuel', '') == 'on'
        insurance = request.POST.get('insurance', '') == 'on'

        if ('fuel' in request.POST and 'insurance' in request.POST):
            additions = priceOfAddi.insurance + priceOfAddi.fuel
        elif 'fuel' in request.POST:
            additions = priceOfAddi.fuel
        elif 'insurance' in request.POST:
            additions = priceOfAddi.insurance
        priceTotal = (int(car.price) * days + additions)

        addingToBase = Order(customer=current, customerID=current.id, carModel=car.model, automobileId=car.id,
                             price=priceTotal, startRent=sdate, endRent=edate, pickUp=place, fullFuel=fuel,
                             insurance=insurance)
        addingToBase.save()
        currentOrder = addingToBase.id

    context = {
        'car': car,
        'fuel': fuel,
        'place': place,
        'endDate': endDate,
        'current': current,
        'insurance': insurance,
        'startDate': startDate,
        'priceTotal': priceTotal,
        'currentOrder': currentOrder,
    }
    return render(request, 'confir.html', context, )


@login_required(login_url='home.html')
def payment(request, pk):
    current = request.user
    phoneAuth = request.POST['phoneCardAuth']
    emailAuth = request.POST['emailCardAuth']
    databaseOrder = Order.objects.get(id=pk)
    pricePennies = (databaseOrder.price * 100)

    if (request.method == 'POST' and phoneAuth == current.customer.phone and emailAuth == current.customer.email):
        customer = stripe.Customer.create(

            email=current.customer.email,
            phone=current.customer.phone,
            description=databaseOrder.customerID,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=pricePennies,
            currency='usd',
            description=pk
        )
        context = {}
        return render(request, 'succes.html', context, )
    else:
        return redirect('confir.html')


@login_required(login_url='home.html')
def cancelOrder(request, pk):
    order = Order.objects.get(id=pk)
    orderForCancel = canceledOrders(payed=order.payed, customerID=order.customerID, price=order.price,
                                    automobileId=order.automobileId)
    orderForCancel.save()
    order.delete()
