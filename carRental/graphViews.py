from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum, Max
from collections import defaultdict, Counter
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required


@login_required(login_url='home.html')
def graph(request):
    dateMoneyList, dataDateMoneyList, locationValues = [], [], []
    format = "%Y/%m/%d"
    current = request.user
    dataHolder = Rental.objects.all()
    location = PlaceToStart.objects.all().values_list('id', 'placeToStart')
    dataHolderPayed = dataHolder.filter(payed=True).values('orderDate', 'price')
    favCar = dataHolder.values('carModel').annotate(car_count=Count('carModel'))
    favPlace = dataHolder.values_list('placeToStart')
    dataCarList = [val for x in favCar for key, val in x.items()]
    placeData = dict(Counter([x for tup in favPlace for x in tup]))

    for x_id, place in location:
        locationValues.append((place, placeData[x_id]))

    for x in dataHolderPayed:
        for key, value in x.items():
            if key == 'orderDate':
                dataDateMoneyList.append(value.strftime(format))
            if key == 'price':
                dateMoneyList.append(value)

    CombinedData = [(i, j) for i, j in zip(dataDateMoneyList, dateMoneyList)]
    sumCombindedData = defaultdict(int)
    for key, val in CombinedData:
        sumCombindedData[key] += val

    # dataCarDict={dataCarList[i]: dataCarList[i + 1] for i in range(0, len(dataCarList), 2)}
    # I don't know why dict itteration doesn't work 9in graph.html that's why we are doing this this way

    dailyDate = list(sumCombindedData.keys())
    dailyMoney = list(sumCombindedData.values())
    orderedCarsName = dataCarList[::2]
    orderedCarsQuantity = dataCarList[1::2]
    placeName = [x[0] for x in locationValues]
    placeQuantity = [x[1] for x in locationValues]

    context = {
        'current': current,
        'dailyDate': dailyDate,
        'dailyMoney': dailyMoney,

        'placeName': placeName,
        'placeQuantity': placeQuantity,

        'orderedCarsName': orderedCarsName,
        'orderedCarsQuantity': orderedCarsQuantity,
    }

    return render(request, 'graph.html', context)
