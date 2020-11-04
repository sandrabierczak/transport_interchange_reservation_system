from django.contrib.auth.models import User
import django_filters
from .models import CarParkingReservation


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


# class ParkingFilter(django_filters.FilterSet):
#     class Meta:
#         model = CarParkingReservation
#         fields = ['reservation_from', 'reservation_to', 'place', ]
