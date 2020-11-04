from math import ceil, floor
from django.utils import timezone
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators, DateTimeRangeField
from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


class BikeStations(models.Model):
    street_name = models.CharField(max_length=128)

    @property
    def name(self):
        return " {}".format(self.street_name)

    def __str__(self):
        return self.name


class Bike(models.Model):
    model_name = models.CharField(max_length=128)
    reserved = models.BooleanField(default=False)
    station = models.ForeignKey(BikeStations, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class BikeReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_point = models.ForeignKey(BikeStations, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)


class CarParking(models.Model):
    number = models.CharField(max_length=100)

    @property
    def name(self):
        return "Place {}".format(self.number)

    def __str__(self):
        return self.name


class CarParkingReservation(models.Model):
    """
    Car Parking reservation, includes methods: price = calculates number of hours multiplied by price per hours,
    duration_print = time spent on car parking place

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dates_range = DateTimeRangeField()
    place = models.ForeignKey(CarParking, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=[
                    ('dates_range', RangeOperators.OVERLAPS),
                    ('place', RangeOperators.EQUAL),
                ],
            )
        ]

    @property
    def date_start(self):
        return self.dates_range.lower.strftime('%d-%m-%Y')

    @property
    def date_end(self):
        return self.dates_range.upper.strftime('%d-%m-%Y')

    @property
    def time_start(self):
        return self.dates_range.lower.strftime('%H:%M')

    @property
    def time_end(self):
        return self.dates_range.upper.strftime('%H:%M')

    @property
    def price(self):
        date_format = '%Y-%m-%d %H:%M'
        date_range = str(self.dates_range)
        date_start = datetime.strptime(date_range[1:17], date_format)
        date_end = datetime.strptime(date_range[22:38], date_format)
        duration = date_end - date_start
        duration_minutes = duration.seconds / 60
        duration_days = duration.days
        if duration_days == 0:
            return round(duration_minutes * 0.05, 2)
        else:
            return round(duration_days * 72 + duration_minutes * 0.05, 2)

    @property
    def duration(self):
        date_format = '%Y-%m-%d %H:%M'
        date_range = str(self.dates_range)
        date_start = datetime.strptime(date_range[1:17], date_format)
        date_end = datetime.strptime(date_range[22:38], date_format)
        duration = date_end - date_start
        duration_days = duration.days
        duration_minutes = ceil(duration.seconds / 60)
        duration_hours = ceil((duration.seconds / 60) / 60)
        return duration_days, duration_minutes, duration_hours

    @property
    def duration_print(self):
        if self.duration[0] == 0 and self.duration[1] < 60:
            return f'{self.duration[1]} minutes '
        elif self.duration[0] == 0 and self.duration[1] > 60:
            return f'{floor(self.duration[1] / 60)} hours {ceil((floor(self.duration[1] / 60) - self.duration[1] / 60) * 60)} minutes '
        else:
            return f'{self.duration[0]} days, {floor(self.duration[1] / 60)} hours {ceil((floor(self.duration[1] / 60) - self.duration[1] / 60) * 60)} minutes '

    @property
    def __str__(self):
        return self.duration_print


class Rating(models.Model):
    """
    Add comments and rates for bikes
    """
    RATES = ((1, "1"),
             (2, "2"),
             (3, "3"),
             (4, "4"),
             (5, "5"),
             )
    rate = models.IntegerField(choices=RATES)
    comments = models.TextField()
    bike = models.ManyToManyField(Bike)
    date_created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
