from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, request, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView
from .forms import LoginUserForm, AddUserForm, CarParkingReservationForm, StationForm, CommentsForm
from .models import CarParkingReservation, CarParking, BikeStations, Bike, BikeReservation, Rating


class MainView(View):
    """Main Page View, user can log in or create account"""

    def get(self, request):
        return render(request, 'base.html')


class AddUserView(FormView):
    """User can register account"""
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = '/'

    def form_valid(self, form):
        """

        :param form:
        :return: If form is valid(email and user don't exist,passwords are equal), then user's account is created
        """
        new_user = form.cleaned_data['username']
        new_password = form.cleaned_data['password2']
        new_email = form.cleaned_data['e_mail']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create_user(username=new_user, first_name=first_name, last_name=last_name,
                                 password=new_password, email=new_email)
        return super(AddUserView, self).form_valid(form)


class LoginUserView(FormView):
    """
    Login user View
    """
    template_name = 'login_user.html'
    form_class = LoginUserForm
    success_url = '/main'

    def form_valid(self, form):
        """

        :param form:
        :return: If form is valid, i.e user and password are correct, else return same form to refill
        """
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            form.add_error('username', 'User or password is incorrect!')
            return self.form_invalid(form)
        return super(LoginUserView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    """Log out View"""

    def get(self, request):
        logout(request)
        message = 'Log out successfully'
        return render(request, 'base.html', {'message': message})


class Desktop(LoginRequiredMixin, View):
    """
    Desktop page, where logged user can see how many reservations have been done,
    Additionally, google map shows current user location.
    """

    def get(self, request):
        """
        :param request:
        :return: Desktop page, where logged user can see how many car parking reservations has been done by user and
        how many bikes were rented in total. If there are no reservations, 0 will be displayed.
        """
        if CarParkingReservation.objects.filter(
                user=self.request.user).count() > 0 or BikeReservation.objects.filter(
            user=self.request.user).count() > 0:
            num_res = CarParkingReservation.objects.filter(user=self.request.user).count()
            num_bike_res = BikeReservation.objects.filter(user=self.request.user).count()
            return render(request, 'main.html',
                          {'num_res': num_res, 'num_bike_res': num_bike_res})
        return render(request, 'main.html', {'num_res': 0, 'num_bike_res': 0})


class CarParkingForm(LoginRequiredMixin, CreateView):
    """
    CarParking Reservation Form, additionally google map show, where parking is located
    """
    form_class = CarParkingReservationForm
    template_name = 'transport/carparkingreservation_form.html'
    success_url = '/main'

    def form_valid(self, form):
        """

        :param form:
        :return: User can select in the form dates range and car parking number place. Dates and place should not
        constrain existing reservations.
        """
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('place', 'Parking is already reserved on this time, Please select another place!')
            return self.form_invalid(form)


class ReservationsList(LoginRequiredMixin, ListView):
    """Shows all users's car parking reservations -places- ordered by date created.
    User can check details of reservation. User can also add new reservation from this view.
    Pagination made by 5 reservations"""
    model = CarParkingReservation
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-date_created')


class ParkingReservationDetail(LoginRequiredMixin, DetailView):
    model = CarParkingReservation

    def parking_details_view(request, pk):
        """
        :param pk:
        :return: Details about parking reservation: place number, cost, duration, reservation dates.
        If carpakring reservations does not exist, http404 response is raised.
        """
        try:
            carparkingreservation = CarParkingReservation.objects.get(pk=pk)
        except CarParkingReservation.DoesNotExist:
            raise Http404('Reservation does not exist')

        return render(request, 'transport/carparkingreservation_detail.html',
                      context={'carparkingreservation': carparkingreservation})


class AddCarParkingPlace(PermissionRequiredMixin, CreateView):
    """
    View with permission for group and superuser. This kind of user can add car parking place.
    """
    permission_required = 'transport.add_carparking'
    model = CarParking
    fields = "__all__"
    success_url = '/main'


class SelectStation(LoginRequiredMixin, View):
    def get(self, request):
        """
        :param request:
        :return: Station Form from where user wants to rent a bike
        """
        form = StationForm
        return render(request, 'transport/locations.html', {'form': form})

    def post(self, request):
        """

        :param request:
        :return: Selected station id and redirects to next step form
        """
        message = 'Please refill form'
        form = StationForm(request.POST)
        if form.is_valid():
            station_id = form.cleaned_data['station']
            station = BikeStations.objects.get(pk=station_id.id)
            return redirect(f'/bike_reservation/{station.id}')
        return render(request, 'transport/locations.html', {'form': form, 'message': message})


class BikeReservationView(LoginRequiredMixin, View):
    template_name = 'transport/bike_reserve.html'

    def get(self, request, station):
        """

        :param request:
        :param station: Station id, selected in previous form
        :return: Form with list of available bikes on selected station. If there are no bikes and stations
        info message is returned.
        """
        try:
            BikeStations.objects.get(pk=station)
        except BikeStations.DoesNotExist:
            raise Http404('BikeStation does not exist')
        if BikeStations.objects.count() > 0 and Bike.objects.count() > 0:
            available_bikes = Bike.objects.filter(station_id=station, reserved=False)
            return render(request, self.template_name, {'available_bikes': available_bikes})
        message = 'There are no stations and bikes in database'
        return render(request, self.template_name, {'message': message})

    def post(self, request, station):
        """

        :param request:
        :param station: Station id, selected in previous form
        :return: Bike reservation and Bike object is updated as reserved
        """
        bike_id = request.POST.get('bike_id')
        user = self.request.user
        BikeReservation.objects.create(bike_id=bike_id, start_point_id=station, user=user)
        bike = Bike.objects.get(pk=bike_id)
        bike.reserved = True
        bike.save()
        return redirect('/main')


class ReservationsBikeList(LoginRequiredMixin, ListView):
    """
    List of currently reserved bikes by logged user.
    User can return bike by clicking bike from list.
    """
    model = BikeReservation
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, bike__reserved=True).order_by('-id')


class ReturnBike(LoginRequiredMixin, View):
    """
    User returns bike selected in previous form and selects station where to return bike.
    """
    template_name = 'transport/return_bike.html'

    def get(self, request, bike):
        """

        :param request:
        :param bike:
        :return: Form that shows all bike stations
        """
        if BikeStations.objects.count() > 0 and Bike.objects.count() > 0:
            stations = BikeStations.objects.all()
            return render(request, self.template_name, {'stations': stations})
        message = 'There are no stations and bikes in database'
        return render(request, self.template_name, {'message': message})

    def post(self, request, bike):
        """
        :param request:
        :param bike: Bike selected for return
        :return: Bike is returned. Bike reserved field is updated on False. Station id is updated.
        """
        try:
            bike = Bike.objects.get(pk=bike)
        except Bike.DoesNotExist:
            raise Http404('Bike does not exist')
        station_id = request.POST['station_id']
        bike.reserved = False
        bike.station_id = station_id
        bike.save()
        return redirect('/main')


class AddCommentsView(LoginRequiredMixin, CreateView):
    """
    User can add comments according to bike condition, suggestions and see comments from other users.
    """
    form_class = CommentsForm
    template_name = 'transport/bike_comments.html'
    success_url = '/comments'
    info_sended = Rating.bike.through.objects.all().order_by('-rating__date_created')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """

        :param kwargs:
        :return: List of all comments, available for all logged users.
        """
        ctx = super(AddCommentsView, self).get_context_data(**kwargs)
        ctx['info_sended'] = Rating.bike.through.objects.all().order_by('-rating__date_created')
        return ctx
