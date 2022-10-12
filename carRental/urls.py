from django.urls import path
from carRental import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = [
    path('carRental/', views.CarCompanyList.as_view()),
    path('carRental/<int:pk>', views.CarCompanyDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns = format_suffix_patterns(urlpatterns)



