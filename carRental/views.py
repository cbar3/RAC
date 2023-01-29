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
from .forms import RegisterForm, CustomerUpdate, ProductUpdate, AddCarForm, LoginForm
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

    # Φίλτρα για τη φόρμα αναζήτησης
    if txt == '':
        cars = Car.objects.all().order_by('carModel')[:12]
    else:
        cars = Car.objects.filter((Q(carModel__contains=txt)
                                   | Q(transmission__contains=txt)
                                   | Q(type__contains=txt)
                                   | Q(manufacturer__manufacturerName__contains=txt)))

    # Ο έλεγχος που γίνεται για να επιστρέψει μόνο τα διαθέσιμα οχήματα. Ο χρήστης επιλέγει ημερομηνία αναχώρησης
    # και ημερομηνία επιστροφής και η σελίδα επιστρέφει μόνο τα αποτελέσματα - τα οχήματα που είναι διαθέσιμα.
    format = "%m/%d/%Y"
    if request.method == 'POST':
        filterStartDate = request.POST['startDate']
        filterEndDate = request.POST['endDate']

        formattedFilterStartDate = datetime.strptime(filterStartDate, format)
        formattedFilterEndDate = datetime.strptime(filterEndDate, format)

        # Φίλτρα ελέγχου για τη διαθεσιμότητα. Σύγκριση της ημερομηνία που επιλέγει ο χρήστης με τις ημερομηνίες των ήδη
        # νοικιασμένων οχημάτων που είναι αποθηκευμένα στη βάση.
        rentals = Rental.objects.filter(
            (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ) | (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ))

        # Αν υπάρχουν διαθέσιμο οχήματα επέστρεψε μια λίστα με τα διαθέσιμα
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

    # Δημιουργία μιας λίστας με τις ημερομηνίες που πρέπει να αποκλειστούν απο το datepicker.
    # Αυτές που δεν είναι διαθέσιμο το όχημα
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
    dataHolder = []
    available_cars = []
    dataClean = []
    current = request.user
    carData = Car.objects.all()
    rawData = Rental.objects.all()

    # Φίλτρα για τη φόρμα αναζήτησης
    if txt == '':
        cars = Car.objects.all().order_by('carModel')
    else:
        cars = Car.objects.filter((Q(carModel__contains=txt)
                                   | Q(transmission__contains=txt)
                                   | Q(type__contains=txt)
                                   | Q(manufacturer__manufacturerName__contains=txt)))

    # Ο έλεγχος που γίνεται για να επιστρέψει μόνο τα διαθέσιμα οχήματα. Ο χρήστης επιλέγει ημερομηνία αναχώρησης
    # και ημερομηνία επιστροφής και η σελίδα επιστρέφει μόνο τα αποτελέσματα - τα οχήματα που είναι διαθέσιμα.

    format = "%m/%d/%Y"
    if request.method == 'POST':
        filterStartDate = request.POST['startDate']
        filterEndDate = request.POST['endDate']

        formattedFilterStartDate = datetime.strptime(filterStartDate, format)
        formattedFilterEndDate = datetime.strptime(filterEndDate, format)

        # Φίλτρα ελέγχου για τη διαθεσιμότητα. Σύγκριση της ημερομηνία που επιλέγει ο χρήστης με τις ημερομηνίες των ήδη
        # νοικιασμένων οχημάτων που είναι αποθηκευμένα στη βάση.
        rentals = Rental.objects.filter(
            (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ) | (
                    Q(startDate__lte=formattedFilterEndDate)
                    & Q(finishDate__gte=formattedFilterStartDate)
            ))

        # Αν υπάρχουν διαθέσιμο οχήματα επέστρεψε μια λίστα με τα διαθέσιμα
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

    # Δημιουργία μιας λίστας με τις ημερομηνίες που πρέπει να αποκλειστούν απο το datepicker.
    # Αυτές που δεν είναι διαθέσιμο το όχημα
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


def user_login(request):
    # view για τη φόρμα εισόδου του χρήστη στην εφαρμογή
    if request.method == 'POST':
        # Γίνεται επεξεργασία του request αν υπάρχουν, έχουν γίνει POST δεδομένα. Username/ password
        username = request.POST['username']
        password = request.POST['password']
        # Έλεγχος αν ο συνδυασμός username και password είναι σωστός
        user = authenticate(username=username, password=password)
        if user is not None:
            # Σώζει το session σε cookie για να μπορέσει να πραγματοποιήσει την είσοδο του χρήστη
            login(request, user)
            # Επιτυχία εισόδου, επιστροφή στη home page
            return render(request, 'home.html')
        else:
            # Μήνυμα λάθος σε περίπτωση που χρησιμοποιηθούν λάθος στοιχεία εισόδου.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # Όταν δεν έχουν μπει στοιχεία εισόδου στη φόρμα τότε επιστρέφει ξανά τη σελίδα εισόδου με τη φόρμα.
        return render(request, 'login.html')


def user_login1(request):
    # view για τη φόρμα εισόδου του χρήστη στην εφαρμογή
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Γίνεται επεξεργασία του request αν υπάρχουν, έχουν γίνει POST δεδομένα. Username/ password
            username = request.POST['username']
            password = request.POST['password']
            # Έλεγχος αν ο συνδυασμός username και password είναι σωστός
            user = authenticate(username=username, password=password)
            if user is not None:
                # Σώζει το session σε cookie για να μπορέσει να πραγματοποιήσει την είσοδο του χρήστη
                login(request, user)
                # Επιτυχία εισόδου, επιστροφή στη home page
                return redirect('home')
        else:
            # Μήνυμα λάθος σε περίπτωση που χρησιμοποιηθούν λάθος στοιχεία εισόδου.
            return render(request, 'login1.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        form = LoginForm
        # Όταν δεν έχουν μπει στοιχεία εισόδου στη φόρμα τότε επιστρέφει ξανά τη σελίδα εισόδου με τη φόρμα.
    return render(request, 'login1.html', {'loginForm': form})


def user_register(request):
    # Το view για τη σελίδα της εγγραφής του χρήστη
    # template = 'register.html'
    template = 'register1.html'
    # Έλεγχος αν είναι μέθοδος POST το request και στη συνέχεια να επεξεργαστούν τα στοιχεία της φόρμας
    if request.method == 'POST':
        # Δημιουργία ενός στιγμιότυπου της φόρμας το οποίο θα τροφοδοτηθεί με δεδομένα απο το POST request
        form = RegisterForm(request.POST)
        # Έλεγχος αν η φόρμα είναι έγκυρη
        if form.is_valid():
            # Έλεγχος αν το username που χρησιμοποιήθηκε υπάρχει στη βάση. Αν έχει ήδη γίνει χρήση απο άλλον χρήστη.
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'register1.html', {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            # Έλεγχος αν το email που χρησιμοποιείται για την εγγραφή υπάρχει ήδη στην βάση.
            # Αν έχει ήδη γίνει χρήση απο άλλον χρήστη.
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, 'register1.html', {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            # Έλεγχος αν το password έχει συμπληρωθεί και στα 2 πεδία που απαιτείται είναι το ίδιο.
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, 'register1.html', {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Αν περάσει απο όλους τους ελέγχους τότε δημιούργησε τον χρήστη - πελάτη.
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

                # Και πλέον κάνε εγγραφή τον χρήστη
                login(request, user)

                # μεταφορά στην αρχική σελίδα
                return HttpResponseRedirect('home')

    # Αν δεν υπάρχουν δεδομένα για POST απλά εμφάνισε την φόρμα
    else:
        form = RegisterForm()

    return render(request, 'register1.html', {'form': form})


@login_required(login_url='home.html')
# Ρουτίνα για έξοδο του χρήστη
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home.html')
# Το view για τη σελίδα κράτησης του οχήματος
def createRental(request, pk):
    dataHolder = []
    dataClean = []
    current = request.user
    carData = Car.objects.get(id=pk)
    pickupPlace = PlaceToStart.objects.all()
    rawData = Rental.objects.filter(carId=pk)
    priceOfAddi = Extras.objects.last()

    # Δημιουργία μιας λίστας με τις ημερομηνίες που πρέπει να αποκλειστούν απο το datepicker.
    # Αυτές που δεν είναι διαθέσιμο το όχημα
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
# View για την επιβεβαίωση της κράτησης. Αποθήκευση στη βάση των στοιχείων της κράτησης.
def order(request, pk):
    car = Car.objects.get(id=pk)
    # Επιβεβαίωση αν η μέθοδος του request είναι POST.
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        current = request.user

    format = "%m/%d/%Y"
    if request.method == 'POST' and endDate > startDate:

        additions = 0
        priceOfAddi = Extras.objects.last()
        sDate = datetime.strptime(startDate, format)
        enDate = datetime.strptime(endDate, format)
        daysTotal = enDate - sDate
        days = int(daysTotal.days)
        place = PlaceToStart.objects.get(id=request.POST['pickUpPlace'])
        fuel = request.POST.get('fuel', '') == 'on'
        insurance = request.POST.get('insurance', '') == 'on'

        # Υπολογισμός της αξίας της μεταβλητής πρόσθετες υπηρεσίες "additions" ανάλογα με τις επιλογές του χρήστη.
        if 'fuel' in request.POST and 'insurance' in request.POST:
            additions = priceOfAddi.insurance + priceOfAddi.fuel
        elif 'fuel' in request.POST:
            additions = priceOfAddi.fuel
        elif 'insurance' in request.POST:
            additions = priceOfAddi.insurance * days
        priceTotal = (int(car.price) * days + additions)

        # Αποθήκευση στην βάση των δεδομένων. Δημιουργία της κράτησης

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
            request.method == 'POST' and phoneAuth == current.costumer.costumerPhoneNumber and emailAuth ==
            current.costumer.costumerEmail):
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
def success(request):
    return render(request, 'success.html')


@login_required(login_url='home.html')
# Το view για την ακύρωση της κράτησης
def cancelOrder(request, pk):
    orderCancel = Rental.objects.get(id=pk)
    orderForCancel = CanceledOrders(payed=orderCancel.payed, costumerID=orderCancel.costumerID, price=orderCancel.price,
                                    carId=orderCancel.carId)

    orderForCancel.save()
    orderCancel.delete()

    return redirect('home')


@login_required(login_url='home.html')
# Το view για το προφίλ του χρήστη
def customerPage(request, pk):
    current = request.user
    dataHolder = Rental.objects.filter(costumerID=current.id)
    totalPrice = list(dataHolder.aggregate(Sum('price')).values())[0]
    orderList = reversed(dataHolder)
    lastOrder = dataHolder.last()
    # Εμφανίζει το αγαπημένο όχημα του χρήστη. Αυτό που έχει κάνει κράτηση τις περισσότερες φορές.
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
# Το view για την ενημέρωση των στοιχείων του χρήστη. Ο χρήστης με την βοήθεια μιας φόρμας μπορεί να ενημερώσει
# τη βάση με τα νέα στοιχεία
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
# Το view της σελίδας που επιστρέφει όλες τις ενοικιάσεις. Μπορεί να τη δεί ο χρήστης υπάλληλος και ο διαχειριστής
def totalRentals(request):
    current = request.user
    rentals = Rental.objects.all()

    context = {
        'current': current,
        'rentals': rentals,
    }
    return render(request, 'totalRentals.html', context)


@login_required(login_url='home.html')
# Το view της σελίδας που επιστρέφει όλες τις ακυρωμένες κρατήσεις. Μπορεί να τη δεί ο χρήστης υπάλληλος και
# ο διαχειριστής
def watchCanceledOrders(request):
    return render(request, 'watchCanceledOrders.html')


@login_required(login_url='home.html')
# Το view που επιστρέφει τη σελίδα διαχείρισης του στόλου οχημάτων στον χρήστη υπάλληλο και στον διαχειριστή.
def watchFleet(request):
    cars = Car.objects.all().order_by('carModel')
    return render(request, 'watchFleet.html', {'cars': cars})


@login_required(login_url='home.html')
# Το view που επιστρέφει τη σελίδα με τις λεπτομέρειες είδους για το κάθε όχημα του στόλου
def watchFleetProductDetails(request, pk):
    cars = get_object_or_404(Car, pk=pk)
    return render(request, 'watchFleetProductDetails.html', {'cars': cars})


@login_required(login_url='home.html')
# Το view για την σελίδα ενημέρωσης των δεδομένων του οχήματος, αν πρέπει να γίνει κάποια αλλαγή.
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
# Το view για τη διαγραφή ενός οχήματος απο την βάση.
def deleteProduct(request, pk):
    deleteCar = Car.objects.get(id=pk)

    deleteCar.delete()

    return redirect('home')


def addCar(request):
    # view για τη δημιουργία - προσθήκη οχήματος στη βάση απο τον χρήστη υπάλληλο και τον διαχειριστή
    template = 'addCar.html'

    if request.method == 'POST':
        # Δημιουργία ενός στιγμιότυπου της φόρμας το οποίο θα τροφοδοτηθεί με δεδομένα απο το POST request
        form = AddCarForm(request.POST, request.FILES)
        # Έλεγχος αν η φόρμα είναι έγκυρη
        if form.is_valid():
            # Έλεγχος αν το μοντέλο του οχήματος υπάρχει ήδη στη βάση.
            if Car.objects.filter(carModel=form.cleaned_data['carModel']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Car Model already exists.'
                })
            else:
                # Δημιουργία που οχήματος. Αποθήκευση στην βάση
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

                # Επιστρέφει στη σελίδα διαχείρισης στόλου
                return HttpResponseRedirect('watchFleet')

    # Αν δεν υπάρχουν δεδομένα για POST απλά εμφάνισε τη φόρμα
    else:
        form = AddCarForm()

    return render(request, template, {'form': form})
