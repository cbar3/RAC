from django.urls import path
from carRental import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = [
    path('carRentalCompany/', views.CarCompanyList.as_view()),
    path('carRentalCompany/<int:pk>', views.CarCompanyDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('car/', views.CarList.as_view()),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('carManufacturer/', views.ManufacturerList.as_view()),
    path('carManufacturer/<int:pk>', views.ManufacturerDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)



