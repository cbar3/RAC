from django.contrib import admin
from . models import RentalCompany, Car, Manufacturer, Costumer, PlaceToStart, Rental

admin.site.register(RentalCompany)
admin.site.register(Car)
admin.site.register(Manufacturer)
admin.site.register(Costumer)
admin.site.register(PlaceToStart)
admin.site.register(Rental)
