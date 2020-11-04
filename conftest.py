import pytest
from django.contrib.auth.models import User
from django.test import Client

from transport.models import CarParking, Bike, BikeStations, BikeReservation, CarParkingReservation, CarParking, Rating


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def carparking():
    carplace = CarParking.objects.create(number=101)
    return carplace


@pytest.fixture
def user():
    user = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                    password='Password1', email='new_email@o2.pl')
    return user
@pytest.fixture
def user2():
    user2 = User.objects.create_user(username='new_user1', first_name='User1', last_name=' ',
                                    password='Password1', email='new_email2@o2.pl')
    return user2

@pytest.fixture
def bikestations():
    bikestation1 = BikeStations.objects.create(street_name='Brynow')
    bikestation2 = BikeStations.objects.create(street_name='Katowice Dworzec')
    bikestation3 = BikeStations.objects.create(street_name='Katowice Dworzec 2')
    return BikeStations.objects.all().order_by('street_name')


@pytest.fixture
def bikestation1():
    bikestation1 = BikeStations.objects.create(street_name='Brynow')
    return bikestation1


@pytest.fixture
def bike():
    bikestation = BikeStations.objects.create(street_name='Dworzec Katowice')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation)
    return bike


@pytest.fixture
def bike_not_reserved():
    bikestation = BikeStations.objects.create(street_name='Dworzec Katowice')
    bike = Bike.objects.create(model_name='Bike_1', reserved=False, station=bikestation)
    return bike, bikestation


@pytest.fixture
def bike_reserved():
    bikestation = BikeStations.objects.create(street_name='Dworzec Katowice')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation)
    return bike, bikestation


@pytest.fixture
def bikes():
    bikestation2 = BikeStations.objects.create(street_name='Dworzec PKP')
    bike = Bike.objects.create(model_name='City bike 1', reserved=True, station=bikestation2)
    bike1 = Bike.objects.create(model_name='City bike 2', reserved=True, station=bikestation2)
    bike3 = Bike.objects.create(model_name='City bike 3', reserved=True, station=bikestation2)
    bike4 = Bike.objects.create(model_name='City bike 4', reserved=True, station=bikestation2)
    return Bike.objects.all()


@pytest.fixture
def bikereservations2():
    user = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                    password='Password1', email='new_email@o2.pl')
    bikestation1 = BikeStations.objects.create(street_name='Brynów')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation1)
    bike1 = Bike.objects.create(model_name='Bike_1', reserved=False, station=bikestation1)
    b = BikeReservation.objects.create(user=user, start_point=bikestation1, bike=bike)
    b2 = BikeReservation.objects.create(user=user, start_point=bikestation1, bike=bike)
    b3 = BikeReservation.objects.create(user=user, start_point=bikestation1, bike=bike1)
    return BikeReservation.objects.all()


@pytest.fixture
def bikereservations():
    user = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                    password='Password1', email='new_email@o2.pl')
    bikestation1 = BikeStations.objects.create(street_name='Brynów')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation1)
    b = BikeReservation.objects.create(user=user, start_point=bikestation1, bike=bike)
    b2 = BikeReservation.objects.create(user=user, start_point=bikestation1, bike=bike)
    return BikeReservation.objects.all().order_by('-id')


@pytest.fixture
def carparkingreservation():
    user1 = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                     password='Password1', email='new_email@o2.pl')
    parkingplace = CarParking.objects.create(number='101')
    reservation = CarParkingReservation.objects.create(user=user1,
                                                       dates_range='[2020-10-29 15:00:00, 2020-10-30 15:00:00)',
                                                       place=parkingplace)
    return reservation


@pytest.fixture
def carparkingreservations():
    user1 = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                     password='Password1', email='new_email@o2.pl')
    user2 = User.objects.create_user(username='new_user2', first_name='User', last_name='XYZ',
                                     password='Password1', email='new_email2@o2.pl')
    parkingplace1 = CarParking.objects.create(number='101')
    parkingplace2 = CarParking.objects.create(number='102')
    reservation1 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-10-21 20:00:00, 2020-10-21 21:30:00)',
                                                        place=parkingplace1)
    reservation2 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-10-21 21:00:00, 2020-10-21 21:47:00)',
                                                        place=parkingplace2)
    reservation3 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-10-23 19:00:00, 2020-11-19 06:00:00)',
                                                        place=parkingplace2)
    reservation4 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-11-22 19:00:00, 2020-11-22 23:45:00)',
                                                        place=parkingplace2)
    return CarParkingReservation.objects.all()


@pytest.fixture
def carparkingreservations6():
    user1 = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                     password='Password1', email='new_email@o2.pl')
    parkingplace1 = CarParking.objects.create(number='101')
    parkingplace2 = CarParking.objects.create(number='102')
    parkingplace3 = CarParking.objects.create(number='103')
    reservation1 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-10-29 15:00:00, 2020-10-30 15:00:00)',
                                                        place=parkingplace1)
    reservation2 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-11-25 17:00:00, 2020-11-25 19:00:00)',
                                                        place=parkingplace2)
    reservation3 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-11-26 17:00:00, 2020-11-29 21:00:00)',
                                                        place=parkingplace3)
    reservation4 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-12-22 17:00:00, 2020-12-29 22:00:00)',
                                                        place=parkingplace1)
    reservation5 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-11-26 17:00:00, 2020-11-29 21:00:00)',
                                                        place=parkingplace1)
    reservation6 = CarParkingReservation.objects.create(user=user1,
                                                        dates_range='[2020-11-22 17:00:00, 2020-11-22 21:00:00)',
                                                        place=parkingplace2)
    return CarParkingReservation.objects.all()


@pytest.fixture
def bikereservations_user_id():
    bikestation1 = BikeStations.objects.create(street_name='Brynów')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation1)
    b = BikeReservation.objects.create(user_id=34, start_point=bikestation1, bike=bike)
    b2 = BikeReservation.objects.create(user_id=34, start_point=bikestation1, bike=bike)
    return BikeReservation.objects.all()


@pytest.fixture
def parking_place():
    parking_place1 = CarParking.objects.create(number='102')
    parking_place2 = CarParking.objects.create(number='103')
    parking_place3 = CarParking.objects.create(number='104')
    return CarParking.objects.all()


@pytest.fixture
def comments():
    bikestation1 = BikeStations.objects.create(street_name='Brynów')
    user = User.objects.create_user(username='new_user', first_name='Sandra', last_name='Bierczak',
                                    password='Password1', email='new_email@o2.pl')
    bike = Bike.objects.create(model_name='Bike_1', reserved=True, station=bikestation1)
    r = Rating.objects.create(rate="1", comments="Bike has destroyed sitting", user=user)
    comment = r.bike.add(bike)
    return comment


@pytest.fixture
def superuser():
    superuser = User.objects.create_superuser(username='super_user', first_name='User', last_name='ZXY',
                                    password='Password', email='super_email@o2.pl')
    return superuser