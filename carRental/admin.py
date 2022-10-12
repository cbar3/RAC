from django.contrib import admin
from . models import RentalCompany, Car, Manufacturer

admin.site.register(RentalCompany)
admin.site.register(Car)
admin.site.register(Manufacturer)


