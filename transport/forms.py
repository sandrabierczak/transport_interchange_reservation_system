import datetime
from django.contrib.auth.models import User
from django import forms
from django.utils.datetime_safe import datetime
from .models import CarParkingReservation, BikeReservation, BikeStations, Rating, Bike, CarParking
from django.forms import ModelForm


class AddUserForm(forms.Form):
    """
    User registration form. Check if password are equal, user and email are not exists in db
    """
    username = forms.CharField(label='Userame', max_length=64)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Name', max_length=64)
    last_name = forms.CharField(label='Surname', max_length=64)
    e_mail = forms.EmailField(label='E-mail', max_length=64)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords are different')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError('User is not available')
        return username

    def clean_e_mail(self):
        e_mail = self.cleaned_data.get('e_mail')
        if e_mail:
            user = User.objects.filter(email=e_mail).exists()
            if user:
                raise forms.ValidationError('Email is already used, please select')
        return e_mail


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CarParkingReservationForm(ModelForm):
    """
    Car parking form, 2 validators, check if date is no from the past and if place exists
    """

    class Meta:
        model = CarParkingReservation
        fields = ['dates_range', 'place']

    def clean_dates_range(self):
        date_reservation = self.cleaned_data.get('dates_range')
        start_date = date_reservation.lower
        if start_date < datetime.now():
            raise forms.ValidationError('Past date')
        return date_reservation

    def clean_place(self):
        place = self.cleaned_data.get('place')
        if place:
            place = CarParking.objects.get(pk=place.id)
            if place:
                return place
        raise forms.ValidationError('Place does no exist!')


class BikeReservationForm(ModelForm):
    class Meta:
        model = BikeReservation
        fields = ['start_point', 'bike']


class StationForm(forms.Form):
    station = forms.ModelChoiceField(BikeStations.objects.all())


class CommentsForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rate', 'comments', 'bike']
