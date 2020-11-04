from .models import CarParking, BikeStations, Bike


def add_car_places():
    for num in range(1, 101):
        CarParking.objects.create(number=num)


def add_bike_station():
    BikeStations.objects.create(street_name="Brynów Pętla")
    BikeStations.objects.create(street_name="Dworzec PkP")


def add_bike():
    for num in range(0, 11):
        Bike.objects.create(model_name=f"City bike {num}", station_id=1)
    for num in range(11, 21):
        Bike.objects.create(model_name=f"City bike {num}", station_id=2)
