from constants import CABINS, CURRENCIES, SEATS, STOPOVERS, FLIGHT_TYPE, SEARCH_TYPE, FLEXIBLE, NIGHTS
from django.db import models
from viewer.models import Profile

import environ




class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, blank=True, default=None)


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=3, blank=True, default=None)
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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    search_type = models.CharField(max_length=10, default='strict', choices=SEARCH_TYPE)
    flight_type = models.CharField(max_length=10, default='round', choices=FLIGHT_TYPE)
    fly_from = models.CharField(max_length=3)
    fly_to = models.CharField(max_length=3)
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    flexible = models.IntegerField(default=0, choices=FLEXIBLE)
    nights_in_dst_from = models.IntegerField(default=7, choices=NIGHTS)
    nights_in_dst_to = models.IntegerField(default=14, choices=NIGHTS)
    max_fly_duration = models.PositiveIntegerField(blank=True, null=True, default=0)
    adults = models.IntegerField(blank=True, default=1, choices=SEATS)
    children = models.IntegerField(blank=True, default=0, choices=SEATS)
    infants = models.IntegerField(blank=True, default=0, choices=SEATS)
    selected_cabins = models.CharField(max_length=1, choices=CABINS, default='M')
    curr = models.CharField(max_length=3, choices=CURRENCIES, default='EUR')
    price_to = models.IntegerField(blank=True, null=True)
    max_stopovers = models.IntegerField(blank=True, null=True, default=None, choices=STOPOVERS)
    limit = models.IntegerField(default=10)
    locale = models.CharField(max_length=5, default='en')


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
    flights = models.ManyToManyField(Flight)
    deep_link = models.CharField(max_length=500)


class Subscription(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)

