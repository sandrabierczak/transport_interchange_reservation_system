from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.db.transaction import TransactionManagementError
from django.http import request
from django.test import TestCase, Client
import pytest
from django.urls import reverse

from transport.models import CarParking, BikeStations, Bike, BikeReservation, CarParkingReservation, Rating
from transport.forms import AddUserForm, StationForm, CarParkingReservationForm

from conftest import client


# MainView test

@pytest.mark.django_db
def test_main_view(client):
    url = ''
    response = client.get(url)
    assert response.status_code == 200


# AddUserView


@pytest.mark.django_db
def test_create_user(client):
    url = '/add_user/'
    assert User.objects.count() == 0
    response = client.post(url, {'username': 'new_user', 'first_name': 'Sandra', 'last_name': 'Bierczak',
                                 'password1': 'Password1', 'password2': 'Password1', 'e_mail': 'new_email@o2.pl'},
                           follow=True)
    assert User.objects.count() == 1
    assert response.status_code == 200
    u = User.objects.get(username='new_user')
    assert u.first_name == 'Sandra'


@pytest.mark.django_db
def test_check_password_form():
    password1 = 'Password1'
    password2 = 'Password2'
    form = AddUserForm(data={'username': 'new_user', 'first_name': 'Sandra', 'last_name': 'Bierczak',
                             'password1': password1, 'password2': password2, 'e_mail': 'new_email@o2.pl'})
    assert form.is_valid() == False


@pytest.mark.django_db
def test_check_if_passwords_are_equal(client):
    url = '/add_user/'
    assert User.objects.count() == 0
    response = client.post(url, {'username': 'new_user', 'first_name': 'Sandra', 'last_name': 'Bierczak',
                                 'password1': 'Password1', 'password2': 'Password2', 'e_mail': 'new_email@o2.pl'})
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_check_if_user_exists(client, user):
    url = '/add_user/'
    assert User.objects.count() == 1
    response = client.post(url, {'username': 'new_user', 'first_name': 'Karolina', 'last_name': 'XYZ',
                                 'password1': 'Password1', 'password2': 'Password1', 'e_mail': 'new_email1@o2.pl'})
    assert response.status_code == 200
    assert User.objects.count() == 1


# ReturnBike Form
@pytest.mark.django_db
def test_check_return_bike_view(client, user, bike):
    client.login(username="new_user", password='Password1')
    url = f'/bike_return/{bike.id}/'
    response = client.get(url)
    bikestation = BikeStations.objects.count()
    bikestation_selected = BikeStations.objects.get(street_name='Dworzec Katowice')
    assert BikeStations.objects.count() == 1
    assert response.status_code == 200
    assert len(response.context['stations']) == bikestation
    assert response.context['stations'][0].id == bikestation_selected.id


@pytest.mark.django_db
def test_check_return_bike_view_no_data(client, user):
    client.login(username="new_user", password='Password1')
    url = f'/bike_return/1/'
    response = client.get(url)
    message = 'There are no stations and bikes in database'
    assert BikeStations.objects.count() == 0
    assert response.status_code == 200
    assert response.context['message'] == message


@pytest.mark.django_db
def test_update_bike_return_view(client, user, bike, bikestations):
    client.login(username="new_user", password='Password1')
    url = f'/bike_return/{bike.id}/'
    # print(BikeStations.objects.all())
    # print(bike.station_id)
    # print(bikestations[3].id)
    response = client.post(url, {'station_id': bikestations[3].id}, follow=True)
    assert response.status_code == 200
    bike.refresh_from_db()
    assert bike.station_id == 5
    assert bike.reserved == False
    # print(bike.station_id)


# Return Bike ListView ReservationsBikeList
@pytest.mark.django_db
def test_return_bike_no_data(client, user):
    client.login(username="new_user", password='Password1')
    url = '/bike_reservations/'
    response = client.get(url)
    assert BikeReservation.objects.count() == 0
    assert response.status_code == 200
    assert 'There are no bike rented.' in str(response.content)


@pytest.mark.django_db
def test_return_bike(client, bikereservations):
    client.login(username="new_user", password='Password1')
    assert BikeReservation.objects.count() == 2
    url = '/bike_reservations/'
    response = client.get(url)
    assert list(response.context['bikereservation_list']) == list(bikereservations)


@pytest.mark.django_db
def test_return_bike_reserved_false(client, bikereservations2):
    client.login(username="new_user", password='Password1')
    assert BikeReservation.objects.count() == 3
    url = '/bike_reservations/'
    response = client.get(url)
    assert len(response.context['bikereservation_list']) == 2
    assert list(response.context['bikereservation_list']) == [bikereservations2[1], bikereservations2[0]]


# Reserve Bike Forms --- SelectStation ---
@pytest.mark.django_db
def test_reserve_bike(client, user, bikestations):
    client.login(username="new_user", password='Password1')
    url = '/bike_reservation/'
    response = client.get(url)
    assert BikeStations.objects.count() == 3
    assert response.status_code == 200
    assert 'Katowice Dworzec 2' in str(response.content)
    assert len(response.context['station']) == 3


@pytest.mark.django_db
def test_check_data_form():
    form = StationForm()
    assert BikeStations.objects.count() == 0
    assert form.is_valid() == False


@pytest.mark.django_db
def test_reserve_bike_from_station_post(client, user, bikestation1):
    client.login(username="new_user", password='Password1')
    url = '/bike_reservation/'
    response = client.post(url, {'station': bikestation1.id}, follow=True)
    assert response.status_code == 200
    assert response.context['station'].street_name == 'Brynow'


@pytest.mark.django_db
def test_reserve_bike_from_station_post(client, user, bikestation1):
    client.login(username="new_user", password='Password1')
    url = '/bike_reservation/'
    response = client.post(url, {'station': 1000})
    assert 'Please refill form' in str(response.content)
    assert response.context['message'] == 'Please refill form'
    assert response.status_code == 200


# Reserve Bike Forms --- BikeReservationView ---
@pytest.mark.django_db
def test_reserve_bike(client, user, bike_not_reserved):
    client.login(username="new_user", password='Password1')
    url = f'/bike_reservation/{bike_not_reserved[1].id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Bike_1' in str(response.content)
    assert len(response.context['available_bikes']) == 1
    assert response.context['available_bikes'][0] == bike_not_reserved[0]


@pytest.mark.django_db
def test_reserve_bike_reserved(client, user, bike_reserved):
    client.login(username="new_user", password='Password1')
    assert Bike.objects.count() == 1
    url = f'/bike_reservation/{bike_reserved[1].id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['available_bikes']) == 0


@pytest.mark.django_db
def test_reserve_bike_station_id_not_exists(client, user):
    client.login(username="new_user", password='Password1')
    url = f'/bike_reservation/300/'
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_reserve_bike_post(client, user, bike_not_reserved):
    client.login(username="new_user", password='Password1')
    assert BikeReservation.objects.count() == 0
    url = f'/bike_reservation/{bike_not_reserved[1].id}/'
    response = client.post(url, {'bike_id': bike_not_reserved[0].id}, follow=True)
    assert response.status_code == 200
    assert BikeReservation.objects.count() == 1
    bike_not_reserved[0].refresh_from_db()
    assert bike_not_reserved[0].reserved == True


# ReservationsList ---
@pytest.mark.django_db
def test_reservation_list(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    url = '/reservation_list/'
    assert CarParkingReservation.objects.count() == 4
    response = client.get(url)
    assert len(response.context['carparkingreservation_list']) == 4
    assert response.status_code == 200
    assert response.context['is_paginated'] == False


@pytest.mark.django_db
def test_reservation_list_pagination(client, carparkingreservations6):
    client.login(username="new_user", password='Password1')
    assert CarParkingReservation.objects.count() == 6
    response = client.get('/reservation_list/?page=2')
    assert len(response.context['carparkingreservation_list']) == 1
    assert response.status_code == 200
    assert response.context['is_paginated'] == True


@pytest.mark.django_db
def test_reservation_list_another_user_logged(client, carparkingreservations):
    client.login(username="new_user2", password='Password1')
    url = '/reservation_list/'
    assert CarParkingReservation.objects.count() == 4
    response = client.get(url)
    assert len(response.context['carparkingreservation_list']) == 0
    assert response.status_code == 200
    assert 'There are no reservations' in str(response.content)


# ParkingReservationDetail ---

@pytest.mark.django_db
def test_reservation_detail_list_no_pk(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    response = client.get('/parking_details/1000/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_reservation_detail_list(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    response = client.get(f'/parking_details/{carparkingreservations[0].id}/')
    assert response.status_code == 200
    response_context = response.context['carparkingreservation']
    assert response_context.place.name == 'Place 101'
    assert response_context.duration_print == '1 hours -30 minutes '
    assert response_context.price == 4.5
    assert response_context.date_start == '21-10-2020'
    # print(response.context['carparkingreservation'].place.name)


@pytest.mark.django_db
def test_reservation_detail_minutes(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    response = client.get(f'/parking_details/{carparkingreservations[1].id}/')
    assert response.status_code == 200
    response_context = response.context['carparkingreservation']
    assert response_context.duration_print == '47 minutes '
    assert response_context.price == 2.35


@pytest.mark.django_db
def test_reservation_detail_days(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    response = client.get(f'/parking_details/{carparkingreservations[2].id}/')
    assert response.status_code == 200
    response_context = response.context['carparkingreservation']
    assert response_context.duration_print == '26 days, 11 hours 0 minutes '
    assert response_context.price == 1905.0


@pytest.mark.django_db
def test_reservation_detail_hours(client, carparkingreservations):
    client.login(username="new_user", password='Password1')
    response = client.get(f'/parking_details/{carparkingreservations[3].id}/')
    assert response.status_code == 200
    response_context = response.context['carparkingreservation']
    assert response_context.duration_print == '4 hours -45 minutes '
    assert response_context.price == 14.25


# AddCarParkingPlace
@pytest.mark.django_db
def test_add_car_place_user(client, user, carparking):
    client.login(username="new_user", password='Password1')
    url = '/add_car_parking/'
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_car_place_superuser(client, superuser):
    client.login(username="super_user", password='Password')
    url = '/add_car_parking/'
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_add_car_place(client, superuser):
#     client.login(username="super_user", password='Password')
#     url = '/add_car_parking/'
#     response = client.post(url, {'number': "110"})
#     assert response.status_code == 302


# LoginUserView
@pytest.mark.django_db
def test_login(client, user):
    response = client.post('/accounts/login/', {'username': 'new_user', 'password': 'Password1'}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_does_not_exists(client):
    response = client.post('/accounts/login/', {'username': 'new_user1', 'password': 'Password1'})
    assert response.status_code == 200
    assert 'User or password is incorrect!' in str(response.content)


@pytest.mark.django_db
def test_login_password_does_not_exists(client, user):
    response = client.post('/accounts/login/', {'username': 'new_user', 'password': 'PasswordDifferent'})
    assert response.status_code == 200
    assert 'User or password is incorrect!' in str(response.content)


# LogoutView
@pytest.mark.django_db
def test_logout(client, user):
    client.login(username="new_user", password='Password1')
    response = client.get('/logout_user/')
    assert response.status_code == 200
    assert 'Log out successfully' in str(response.content)


@pytest.mark.django_db
def test_logout_user_not_logged(client):
    response = client.get('/logout_user/', follow=True)
    assert response.status_code == 200
    assert 'Please register or log in!' in str(response.content)


# Desktop
@pytest.mark.django_db
def test_dashboard(client, bikereservations_user_id, carparkingreservations6):
    client.login(username="new_user", password='Password1')
    assert BikeReservation.objects.count() == 2
    assert CarParkingReservation.objects.count() == 6
    response = client.get('/main/')
    assert response.status_code == 200
    assert response.context['num_res'] == 6
    assert response.context['num_bike_res'] == 2


@pytest.mark.django_db
def test_dashboard_no_data_in_db(client, user):
    client.login(username="new_user", password='Password1')
    assert BikeReservation.objects.count() == 0
    assert CarParkingReservation.objects.count() == 0
    response = client.get('/main/')
    assert response.status_code == 200
    assert response.context['num_res'] == 0
    assert response.context['num_bike_res'] == 0


# CarParkingForm
@pytest.mark.django_db
def test_car_parking_reserve(client, user, parking_place):
    client.login(username="new_user", password='Password1')
    response = client.get('/car_parking/')
    assert response.status_code == 200
    assert CarParking.objects.count() == 3
    assert 'Place 102' in str(response.content)
    assert 'Place 103' in str(response.content)
    assert 'Place 104' in str(response.content)


@pytest.mark.django_db
def test_car_parking_reservation(client, user):
    assert CarParkingReservation.objects.count() == 0
    parkingplace = CarParking.objects.create(number='101')
    client.login(username="new_user", password='Password1')
    response = client.post('/car_parking/',
                           {'dates_range_0': '2020-11-22 21:30', 'dates_range_1': '2020-11-22 23:00',
                            'place': parkingplace.id}, follow=True)
    assert CarParkingReservation.objects.count() == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_car_parking_reservation_past_date(client, user):
    assert CarParkingReservation.objects.count() == 0
    parkingplace = CarParking.objects.create(number='101')
    client.login(username="new_user", password='Password1')
    response = client.post('/car_parking/',
                           {'dates_range_0': '2020-09-22 21:30', 'dates_range_1': '2020-11-22 23:00',
                            'place': parkingplace.id})
    assert CarParkingReservation.objects.count() == 0
    assert 'Past date' in str(response.content)


@pytest.mark.django_db
def test_car_parking_reservation_end_date_before_start_date(client, user):
    assert CarParkingReservation.objects.count() == 0
    parkingplace = CarParking.objects.create(number='101')
    client.login(username="new_user", password='Password1')
    response = client.post('/car_parking/',
                           {'dates_range_0': '2020-11-22 21:30', 'dates_range_1': '2020-11-09 23:00',
                            'place': parkingplace.id})
    assert CarParkingReservation.objects.count() == 0
    assert 'The start of the range must not exceed the end of the range.' in str(response.content)


@pytest.mark.django_db
def test_car_parking_reservation_exists(client, carparkingreservations6):
    parkingplace = CarParking.objects.get(pk=29)
    with pytest.raises(TransactionManagementError):
        assert CarParkingReservation.objects.count() == 6
        client.login(username="new_user", password='Password1')
        response = client.post('/car_parking/',
                               {'dates_range_0': '2020-11-22 19:00', 'dates_range_1': '2020-11-22 22:45',
                                'place': parkingplace.id})
        assert CarParkingReservation.objects.count() == 6
        assert 'Parking is already reserved on this time, Please select another place!' in str(response.content)


@pytest.mark.django_db
def test_car_parking_reservation_no_id(client, user):
    assert CarParkingReservation.objects.count() == 0
    client.login(username="new_user", password='Password1')
    response = client.post('/car_parking/',
                           {'dates_range_0': '2020-11-22 21:30', 'dates_range_1': '2020-11-22 23:00',
                            'place': 10000}, follow=True)
    assert CarParkingReservation.objects.count() == 0
    assert response.status_code == 200


# AddCommentsView
@pytest.mark.django_db
def test_add_comment_get(client, user, bikes):
    client.login(username="new_user", password='Password1')
    url = '/comments/'
    assert Rating.objects.count() == 0
    assert Rating.bike.through.objects.count() == 0
    response = client.post(url, {'rate': "1", 'comments': "ok",
                                 'bike': bikes[0].id}, follow=True)

    assert Rating.objects.count() == 1
    assert Rating.bike.through.objects.count() == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_comment_list(client, comments):
    client.login(username="new_user", password='Password1')
    assert Rating.objects.count() == 1
    assert Rating.bike.through.objects.count() == 1
    url = '/comments/'
    response = client.get(url)
    assert len(response.context['info_sended']) == 1
    assert response.context['info_sended'][0].rating.comments == 'Bike has destroyed sitting'


@pytest.mark.django_db
def test_no_comment_view(client, user):
    client.login(username="new_user", password='Password1')
    url = '/comments/'
    response = client.get(url)
    assert 'There are no comments yet' in str(response.content)
    assert Rating.objects.count() == 0
    assert Rating.bike.through.objects.count() == 0
