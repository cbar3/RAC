from django.urls import path
from carRental import views, pdfViews
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('carList/', views.carlist, name='carList'),
    path('carDetails/<int:pk>', views.cardetail, name='rental'),

    path('login/', views.user_login, name='login'),
    path('login1/', views.user_login1, name='login1'),
    path('login/home', views.home, name='loginHome'),
    path('register/', views.user_register, name='register'),
    path('register1/', views.user_register, name='register1'),
    path('register/home', views.home, name='registerHome'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/<str:pk>/', views.customerPage, name='customer'),
    path('updateView/', views.updateView, name='updateView'),

    path('AdminTools/', views.adminTools, name='pathUrlsAdmin'),
    path('totalRentals/', views.totalRentals, name='totalRentals'),
    path('watchFleet/', views.watchFleet, name='watchFleet'),
    path('addCar/watchFleet/', views.watchFleet, name='addCar/watchFleet'),
    path('watchFleetProductDetails/<int:pk>', views.watchFleetProductDetails, name='watchFleetProductDetails'),
    path('updateProduct/<str:pk>', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<str:pk>/', views.deleteProduct, name='deleteProduct'),
    path('addCar/', views.addCar, name='addCar'),

    path('createRental/<str:pk>/', views.createRental, name='createRental'),
    path('order/<str:pk>/', views.order, name='order'),
    path('success/', views.success, name='success'),
    path('payment/<str:pk>/', views.payment, name='payment'),
    path('cancelOrder/<str:pk>/', views.cancelOrder, name='cancelOrder'),

    path('pdfView/<str:pk>/', pdfViews.ViewPDF.as_view(), name="pdfView"),
    path('pdfDownload/<str:pk>/', pdfViews.DownloadPDF.as_view(), name="pdfDownload"),

    path('carRentalCompany/', views.CarCompanyList.as_view(), name="Car_Rental_Company"),
    path('carRentalCompany/<int:pk>', views.CarCompanyDetail.as_view()),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('car/', views.CarList.as_view(), name="carviewlist"),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('carManufacturer/', views.ManufacturerList.as_view(), name="Manufacturer"),
    path('carManufacturer/<int:pk>', views.ManufacturerDetail.as_view()),
    path('Rental/', views.RentalList.as_view(), name="Rental"),
    path('Rental/<int:pk>', views.RentalDetail.as_view()),
    path('Costumer/', views.CustomerList.as_view(), name="Costumer"),
    path('Costumer/<int:pk>', views.CustomerDetail.as_view()),
    path('PlaceToStart/', views.PlaceToStartList.as_view(), name="PlaceToStart"),
    path('PlaceToStart/<int:pk>', views.PlaceToStartDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
