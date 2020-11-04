"""transport_interchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from transport.views import MainView, AddUserView, LoginUserView, LogoutView, CarParkingForm, Desktop, \
    ReservationsList, ParkingReservationDetail, AddCarParkingPlace, SelectStation, BikeReservationView, \
    ReservationsBikeList, ReturnBike, AddCommentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('accounts/login/', LoginUserView.as_view(), name="login-user"),
    path('logout_user/', LogoutView.as_view(), name="logout-user"),
    path('car_parking/', CarParkingForm.as_view(), name="car_parking"),
    path('add_car_parking/', AddCarParkingPlace.as_view(), name="add_car_parking"),
    path('main/', Desktop.as_view(), name="desktop"),
    path('reservation_list/', ReservationsList.as_view(), name="reservations"),
    path('parking_details/<int:pk>/', ParkingReservationDetail.as_view(), name="car-reservation"),
    path('bike_reservation/', SelectStation.as_view(), name="bike-reservations"),
    path('bike_reservation/<int:station>/', BikeReservationView.as_view(), name="bike-reservations-details"),
    path('bike_reservations/', ReservationsBikeList.as_view(), name="bike-reservations-list"),
    path('bike_return/<int:bike>/', ReturnBike.as_view(), name="bike-return"),
    path('comments/', AddCommentsView.as_view(), name="comments"),
    # url(r'^search/$', search, name='search'),
    # url(r'^parking/$', CarParking, name='car'),
]
