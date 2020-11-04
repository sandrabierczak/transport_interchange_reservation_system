from django.contrib import admin

# Register your models here.
from transport.models import CarParking, Bike

admin.site.register(CarParking)
admin.site.register(Bike)
