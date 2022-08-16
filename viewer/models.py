from django.db import models
from django.contrib.auth.models import User
from constants import CABINS, CURRENCIES


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)


class City(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)


class Airport(models.Model):
    iata_code = models.CharField(max_length=3, primary_key=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)


class Airline(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    logo = models.ImageField(upload_to='airline_logos', blank=True)


class Flight(models.Model):
    search = models.ForeignKey('Search', on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
    flight_no = models.CharField(max_length=10)
    fly_from = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='fly_from')
    fly_to = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='fly_to')
    local_arrival = models.DateTimeField()
    local_departure = models.DateTimeField()
    fare_category = models.CharField(max_length=1)
    segment_no = models.IntegerField()
    return_flight = models.BooleanField()


class Search(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    fly_from = models.ManyToManyField(Airport, related_name='flight_origin')
    fly_to = models.ManyToManyField(Airport, related_name='flight_destination')
    date_from = models.DateField()
    date_to = models.DateField()
    return_from = models.DateField(blank=True, null=True)
    return_to = models.DateField(blank=True, null=True)
    nights_in_dst_from = models.IntegerField(blank=True, null=True)
    nights_in_dst_to = models.IntegerField(blank=True, null=True)
    max_fly_duration = models.IntegerField(blank=True, null=True)
    flight_type = models.CharField(max_length=10, default="round")
    adults = models.IntegerField(blank=True, null=True, default=1)
    children = models.IntegerField(blank=True, default=0)
    infants = models.IntegerField(blank=True, default=0)
    selected_cabins = models.CharField(max_length=1, choices=CABINS, default="M")
    mix_with_cabins = models.CharField(max_length=5, choices=CABINS, blank=True, null=True)
    curr = models.CharField(max_length=3, choices=CURRENCIES, default="EUR")
    price_from = models.IntegerField(blank=True, null=True)
    price_to = models.IntegerField(blank=True, null=True)
    max_stopovers = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(default=100)


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    airlines = models.ManyToManyField(Airline)
    fly_from = models.ForeignKey(Airport, related_name='search_origin', on_delete=models.CASCADE)
    fly_to = models.ForeignKey(Airport, related_name='search_destination', on_delete=models.CASCADE)
    departure_duration = models.IntegerField()
    return_duration = models.IntegerField()
    departure_date = models.DateField()
    return_date = models.DateField()
    departure_time = models.TimeField()
    return_time = models.TimeField()
    has_airport_change = models.BooleanField()
    number_of_stops = models.IntegerField()
    price = models.IntegerField()
    bags_price = models.CharField(max_length=100)
    availability = models.IntegerField()
    deep_link = models.CharField(max_length=500)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True, default=None)
    home_airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING)
