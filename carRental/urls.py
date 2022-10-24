from django.urls import path
from carRental import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.car, name='car_list'),
    path('carRentalCompany/', views.CarCompanyList.as_view()),
    path('carRentalCompany/<int:pk>', views.CarCompanyDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('car/', views.CarList.as_view()),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('carManufacturer/', views.ManufacturerList.as_view()),
    path('carManufacturer/<int:pk>', views.ManufacturerDetail.as_view()),
    path('Rental/', views.RentalList.as_view()),
    path('Rental/<int:pk>', views.RentalDetail.as_view()),
    path('Costumer/', views.CustomerList.as_view()),
    path('Costumer/<int:pk>', views.CustomerDetail.as_view()),
    path('PlaceToStart/', views.PlaceToStartList.as_view()),
    path('PlaceToStart/<int:pk>', views.PlaceToStartDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
