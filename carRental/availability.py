import datetime
from carRental.models import Car, Rental


def check_availability(car, check_in, check_out):
    avail_list = []
    booking_list = Rental.objects.filter(car=car)
    for booking in booking_list:
        if booking.startDate > check_out or booking.finishDate < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
