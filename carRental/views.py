# Αρχείο views.py, περιέχει όλα τα function που καλούνται απο την εφαρμογή με τη βοήθεια των http requests
# και http responses.
# Βιβλιοθήκες και επεκτάσεις πυο χρησιμοποιήθηκαν στο αρχείο views.py

from django.contrib.auth import authenticate, login, logout
from carRental.models import RentalCompany, Car, Manufacturer, Rental, Costumer, PlaceToStart, Extras, CanceledOrders
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
from .forms import RegisterForm, CustomerUpdate, ProductUpdate, AddCarForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, timedelta, date
from json import dumps
import stripe
import itertools
from django.contrib import messages
from django.db.models import Count, Sum, Max, Q
from carRental.availability import check_availability


# Οι παρακάτω κλάσεις έχουν δημιουργηθεί για τις ανάγκες του rest api framework και ουσιαστικά κάνουν serialize
# της κλάσεις της βάσης. Επίσης, έχουν μπει κάποια permission ανάλογα με τον χρήστη που συνδέεται στο rest framework,
# έχουν μπει κάποια φίλτρα και η δυνατότητα αναζήτησης και διάταξης των αποτελεσμάτων.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'


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
    filter_fields = (
        'companyName', 'companyAddress', 'companyPhoneNumber', 'companyEmail', 'costumer', 'car', 'placeToStart')
    search_fields = '__all__'
    ordering_fields = '__all__'

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('carModel', 'manufacturer', 'type', 'transmission', 'owner', 'price', 'insurance', 'tank')
    search_fields = '__all__'
    ordering_fields = '__all__'

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('manufacturerName', 'owner')
    search_fields = '__all__'
    ordering_fields = '__all__'

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = (
        'user', 'costumerFirstName', 'costumerLastName', 'costumerEmail', 'costumerPhoneNumber', 'costumerAFM')
    search_fields = '__all__'
    ordering_fields = '__all__'

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RentalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class PlaceToStartList(generics.ListCreateAPIView):
    queryset = PlaceToStart.objects.all()
    serializer_class = PlaceToStartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceToStartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaceToStart.objects.all()
    serializer_class = PlaceToStartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# Το view της αρχικής σελίδας της εφαρμογής (home page), υπάρχει η δυνατότητα αναζήτησης με χρήση text που μπορεί
# να επιστρέψει αποτελέσματα στην οθόνη ανάλογα με τη λέξη κλειδί που έχει χρησιμοποιηθεί.
# Δυνατότητα αναζήτησης διαθέσιμου οχήματος με βάση την ημερομηνία που θέλει ο χρήστης να πραγματοποιήσει την ενοικίαση,
# μας επιστρέφει μόνο τα οχήματα που είναι διαθέσιμα προς ενοικίαση.

def home(request):
    txt = request.GET.get('txt', '')
    dataHolder = []
    dataClean = []
    available_cars = []
    current = request.user
    carData = Car.objects.all()
    rawData = Rental.objects.all()
    priceOfAddi = Extras.objects.last()

    if txt == '':
        cars = Car.objects.all().order_by('carModel')[:12]
    else:
        cars = Car.objects.filter((Q(carModel__contains=txt)
                                   | Q(transmission__contains=txt)
                                   | Q(type__contains=txt)
                                   | Q(manufacturer__manufacturerName__contains=txt)))

    format = "%m/%d/%Y"
    if request.method == 'POST':
        filterStartDate = request.POST['startDate']
        filterEndDate = request.POST['endDate']

        formattedFilterStartDate = datetime.strptime(filterStartDate, format)
        formattedFilterEndDate = datetime.strptime(filterEndDate, format)

        rentals = Rental.objects.filter(
            (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ) | (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ))

        for x in carData:
            available = True

            for y in rentals:
                if y.carId == x.id:
                    available = False
            if available:
                available_cars.append(x.id)

        carsCopy = []

        for x in carData:
            if available_cars.__contains__(x.id):
                carsCopy.append(x)

        cars = carsCopy

    for x in rawData:
        if x.finishDate > datetime.now().date():
            srtDate = x.startDate
            endDate = x.finishDate
            delta = endDate - srtDate
            dataHolder = [(srtDate + timedelta(days=i)) for i in range(delta.days + 1)]

    dataClean = [x.strftime("%d/%m/%Y") for x in dataHolder]
    dataClean = dumps(dataClean)

    context = {
        'cars': cars,
        'current': current,
        'carData': carData,
        'dataClean': dataClean,
    }

    return render(request, 'home.html', context)


# Το view της σελίδας όλα τα οχήματα (car list) μας επιστρέφει όλα τα οχήματα που υπάρχουν. Τα φίλτρα εδώ είναι τα ίδια
# με την αρχική σελίδα.

def carlist(request):
    txt = request.GET.get('txt', '')
    # startDate = request.Get.get['startDate', '']
    # endDate = request.GEt.get['endDate', '']
    dataHolder = []
    available_cars = []
    dataClean = []
    current = request.user
    carData = Car.objects.all()
    rawData = Rental.objects.all()
    # cars = Car.objects.all().order_by('carModel')

    if txt == '':
        cars = Car.objects.all().order_by('carModel')
    else:
        cars = Car.objects.filter((Q(carModel__contains=txt)
                                   | Q(transmission__contains=txt)
                                   | Q(type__contains=txt)
                                   | Q(manufacturer__manufacturerName__contains=txt)))
    """
    if 'startDate' in request.POST and 'finishDate' in request.POST:
        for x in carData:
            if check_availability(x.car, x.startDate['check_in'], x.finishDate['check_out']):
                available_cars.append(x.car)
            if len(available_cars) > 0:
                cars = available_cars[0]
        """
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        current = request.user

    format = "%m/%d/%Y"
    if request.method == 'POST' and endDate > startDate:

        startDate = datetime.strptime(startDate, format)
        endDate = datetime.strptime(endDate, format)
        if startDate == '':
            cars = Rental.objects.all().order_by('carModel')
        if 'startDate' in request.POST and 'finishDate' in request.POST:
            for x in carData:
                if check_availability(x.car, startDate['check_in'], endDate['check_out']):
                    available_cars.append(x.car)
                if len(available_cars) > 0:
                    cars = available_cars[0]

    # making a list of blocked days for date picker

    for x in rawData:
        if x.finishDate > datetime.now().date():
            srtDate = x.startDate
            endDate = x.finishDate
            delta = endDate - srtDate
            dataHolder = [(srtDate + timedelta(days=i)) for i in range(delta.days + 1)]

    dataClean = [x.strftime("%d/%m/%Y") for x in dataHolder]
    dataClean = dumps(dataClean)

    context = {
        'cars': cars,
        'current': current,
        'carData': carData,
        'dataClean': dataClean,
    }

    return render(request, 'carlist.html', context)


# Το view που μας επιστρέφει τη σελίδα με τις λεπτομέρειες για ένα όχημα. Επίσης, ο χρήστης μπορεί να στείλει ένα email
# στην εταιρία ενοικιάσεων όπου μπορεί να ενημερώνει για την εκδήλωση ενδιαφέροντος που έχει. Τέλος, στο κάτω μέρος της
# σελίδας εμφανίζονται σχετικά αποτελέσματα με επιπλέον προτεινόμενα οχήματα.

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
            ['cbarbas82@gmail.com'],
            fail_silently=False
        )

    context = {'cars': cars,
               'carRelated': carRelated}
    return render(request, 'cardetails.html', context)


# view για τη φόρμα εισόδου του χρήστη στην εφαρμογή

def user_login(request):
    if request.method == 'POST':
        # Γίνεται επεξεργασία του request αν υπάρχουν, έχουν γίνει POST δεδομένα. Username/ password
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Έλεγχος αν ο συνδυασμός username και password είναι σωστός
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Σώζει το session σε cookie για να μπορέσει να πραγματοποιήσει την είσοδο του χρήστη
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'home.html')
        else:
            # Μήνυμα λάθος σε περίπτωση που χρησιμοποιηθούν λάθος στοιχεία εισόδου.
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # Όταν δεν έχουν μπει στοιχεία εισόδου στη φόρμα τότε επιστρέφει ξανά τη σελίδα εισόδου με τη φόρμα.
        # No post data available, let's just show the page to the user.
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
                user.save()

                costumer = Costumer(user=user,
                                    costumerFirstName=form.cleaned_data['first_name'],
                                    costumerLastName=form.cleaned_data['last_name'],
                                    costumerEmail=form.cleaned_data['email'],
                                    costumerPhoneNumber=form.cleaned_data['phone_number'],
                                    costumerAFM=form.cleaned_data['AFM'],

                                    )
                costumer.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return HttpResponseRedirect('home')

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
    # global fuel, place, insurance, priceTotal, currentOrder, current
    car = Car.objects.get(id=pk)
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        current = request.user

    format = "%m/%d/%Y"
    if (request.method == 'POST' and endDate > startDate):

        additions = 0
        priceOfAddi = Extras.objects.last()
        sDate = datetime.strptime(startDate, format)
        enDate = datetime.strptime(endDate, format)
        daysTotal = enDate - sDate
        days = int(daysTotal.days)
        place = PlaceToStart.objects.get(id=request.POST['pickUpPlace'])
        fuel = request.POST.get('fuel', '') == 'on'
        insurance = request.POST.get('insurance', '') == 'on'

        if ('fuel' in request.POST and 'insurance' in request.POST):
            additions = priceOfAddi.insurance + priceOfAddi.fuel
        elif 'fuel' in request.POST:
            additions = priceOfAddi.fuel
        elif 'insurance' in request.POST:
            additions = priceOfAddi.insurance * days
        priceTotal = (int(car.price) * days + additions)

        addingToBase = Rental(costumer=current.costumer, costumerID=current.id, customerName=current.costumer.user,
                              car=car, carId=car.id, carModel=car.carModel,
                              price=priceTotal, startDate=sDate, finishDate=enDate, placeToStart=place, fullFuel=fuel,
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
    return render(request, 'order.html', context, )


@login_required(login_url='home.html')
def payment(request, pk):
    current = request.user
    phoneAuth = request.POST['phoneCardAuth']
    emailAuth = request.POST['emailCardAuth']
    databaseOrder = Rental.objects.get(id=pk)
    pricePennies = (databaseOrder.price * 100)

    if (
            request.method == 'POST' and phoneAuth == current.costumer.costumerPhoneNumber and emailAuth == current.costumer.costumerEmail):
        customer = stripe.Customer.create(

            email=current.costumer.costumerEmail,
            phone=current.costumer.costumerPhoneNumber,
            description=databaseOrder.customerID,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=pricePennies,
            currency='euro',
            description=pk
        )
        context = {}
        return render(request, 'success.html', context, )
    else:
        return redirect('order.html')


@login_required(login_url='home.html')
def cancelOrder(request, pk):
    orderCancel = Rental.objects.get(id=pk)
    orderForCancel = CanceledOrders(payed=orderCancel.payed, costumerID=orderCancel.costumerID, price=orderCancel.price,
                                    carId=orderCancel.carId)

    orderForCancel.save()
    orderCancel.delete()

    return redirect('home')


@login_required(login_url='home.html')
def customerPage(request, pk):
    current = request.user
    dataHolder = Rental.objects.filter(costumerID=current.id)
    totalPrice = list(dataHolder.aggregate(Sum('price')).values())[0]
    orderList = reversed(dataHolder)
    lastOrder = dataHolder.last()
    favCar = dataHolder.values('carModel').annotate(car_count=Count('carModel'))
    if not favCar:
        favCarList = "Rent something ;)"
    else:
        favCarList = list(favCar.aggregate(Max('carModel')).values())
        favCarList = favCarList[0].replace("['']", '')

    context = {
        'current': current,
        'orderList': orderList,
        'lastOrder': lastOrder,
        'totalPrice': totalPrice,
        'favCarList': favCarList,
        'dataHolder': dataHolder,
    }
    return render(request, 'customer.html', context)


@login_required(login_url='home.html')
def updateView(request):
    current = request.user

    if request.method == 'POST':
        updateForm = CustomerUpdate(request.POST, request.FILES, instance=current.costumer)
        if updateForm.is_valid():
            updateForm.save()
            return redirect('home')
    else:
        updateForm = CustomerUpdate(instance=current.costumer)
    context = {
        'current': current,
        'updateForm': updateForm,
    }
    return render(request, 'updateCostumer.html', context)


@login_required(login_url='home.html')
def adminTools(request):
    return render(request, 'pathUrlsAdmin.html')


@login_required(login_url='home.html')
def totalRentals(request):
    current = request.user
    rentals = Rental.objects.all()

    context = {
        'current': current,
        'rentals': rentals,
    }
    return render(request, 'totalRentals.html', context)


@login_required(login_url='home.html')
def watchCanceledOrders(request):
    return render(request, 'watchCanceledOrders.html')


@login_required(login_url='home.html')
def watchFleet(request):
    cars = Car.objects.all().order_by('carModel')
    return render(request, 'watchFleet.html', {'cars': cars})


@login_required(login_url='home.html')
def watchFleetProductDetails(request, pk):
    cars = get_object_or_404(Car, pk=pk)
    return render(request, 'watchFleetProductDetails.html', {'cars': cars})


@login_required(login_url='home.html')
def updateProduct(request, pk):
    cars = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        updateForm = ProductUpdate(request.POST, request.FILES, instance=cars)
        if updateForm.is_valid():
            updateForm.save()
            return redirect('watchFleetProductDetails', pk=cars.pk)
    else:
        updateForm = ProductUpdate(instance=cars)
    context = {
        'cars': cars,
        'updateForm': updateForm,
    }
    return render(request, 'updateProduct.html', context)


@login_required(login_url='home.html')
def deleteProduct(request, pk):
    deleteCar = Car.objects.get(id=pk)

    deleteCar.delete()

    return redirect('home')


def addCar(request):
    template = 'addCar.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddCarForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if Car.objects.filter(carModel=form.cleaned_data['carModel']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Car Model already exists.'
                })
            else:
                # Create the car:
                car = Car.objects.create(
                    form.cleaned_data['carModel'],
                    form.cleaned_data['manufacturer'],
                    form.cleaned_data['type'],
                    form.cleaned_data['transmission'],
                    form.cleaned_data['price'],
                    form.cleaned_data['insurance'],
                    form.cleaned_data['tank'],
                    form.cleaned_data['carImage'],
                )
                car.save()

                # redirect to watchFleet page:
                return HttpResponseRedirect('watchFleet')

    # No post data availabe, let's just show the page.
    else:
        form = AddCarForm()

    return render(request, template, {'form': form})
