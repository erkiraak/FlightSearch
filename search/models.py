from constants import CABINS, CURRENCIES, SEATS, STOPOVERS, FLIGHT_TYPE, SEARCH_TYPE, FLEXIBLE, NIGHTS
from django.db import models
from datetime import datetime, timedelta
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
    name = models.CharField(max_length=50, null=True, blank=True)           # TODO add airline API call
    code = models.CharField(max_length=2)
    logo = models.ImageField(upload_to='airline_logos', blank=True)

    @classmethod
    def add_airline_by_code(cls, code):
        return cls.objects.create(code=code)

    @classmethod
    def get_airline(cls, code):
        if cls.objects.filter(code=code).exists():
            return cls.objects.filter(code=code).first()
        else:
            return cls.add_airline_by_code(code)


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

    @classmethod
    def create_flight_object_from_kiwi_response(cls, api_response):
        pass                                                                                    # TODO finish


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
    max_fly_duration = models.PositiveIntegerField(blank=True, null=True, default=None)
    adults = models.IntegerField(blank=True, default=1, choices=SEATS)
    children = models.IntegerField(blank=True, default=0, choices=SEATS)
    infants = models.IntegerField(blank=True, default=0, choices=SEATS)
    selected_cabins = models.CharField(max_length=1, choices=CABINS, default='M')
    curr = models.CharField(max_length=3, choices=CURRENCIES, default='EUR')
    price_to = models.IntegerField(blank=True, null=True)
    max_stopovers = models.IntegerField(blank=True, null=True, default=None, choices=STOPOVERS)
    limit = models.IntegerField(default=10)
    locale = models.CharField(max_length=5, default='en')

    @classmethod
    def create_search_object_from_request(cls, request):
        '''
        Creates a search object from request.GET
        :param request:
        :return: Search object
        '''

        parameters = request.GET

        if request.user.is_authenticated:
            user = Profile.objects.get(user=request.user)
        else:
            user = None

        search = cls(
            user=user,
            flight_type=parameters.get('flight_type'),
            search_type=parameters.get('search_type'),
            fly_from=parameters.get('fly_from'),
            fly_to=parameters.get('fly_to'),
            departure_date=parameters.get('departure_date'),
            return_date=parameters.get('return_date'),
            nights_in_dst_from=parameters.get('nights_in_dst_from'),
            nights_in_dst_to=parameters.get('nights_in_dst_to'),
            max_fly_duration=parameters.get('max_fly_duration'),
            max_stopovers=parameters.get('max_stopovers'),
            adults=parameters.get('adults'),
            children=parameters.get('children'),
            infants=parameters.get('infants'),
            selected_cabins=parameters.get('selected_cabins'),
            curr=parameters.get('curr'),
            price_to=parameters.get('price_to'),
            limit=parameters.get('limit'),
            locale=request.LANGUAGE_CODE,
        )
        return search


class Result(models.Model):
    # search = models.ForeignKey(Search, on_delete=models.CASCADE)
    airlines = models.ManyToManyField(Airline)
    fly_from = models.ForeignKey(Airport, related_name='search_origin', on_delete=models.CASCADE)
    fly_to = models.ForeignKey(Airport, related_name='search_destination', on_delete=models.CASCADE)
    departure_duration = models.DurationField()
    return_duration = models.DurationField()
    departure_date = models.DateField()
    return_date = models.DateField()
    departure_time = models.TimeField()
    departure_arrival_time = models.TimeField()
    return_time = models.TimeField()
    return_arrival_time = models.TimeField()
    connecting_airport_departure = models.ManyToManyField(Airport, related_name='connecting_airport_departure')
    connecting_airport_return = models.ManyToManyField(Airport, related_name='connecting_airport_return')
    has_airport_change = models.BooleanField()
    number_of_stops_departure = models.IntegerField()
    number_of_stops_return = models.IntegerField()
    price = models.IntegerField()
    flights = models.ManyToManyField(Flight)
    booking_token = models.CharField(max_length=1000)

    @classmethod
    def create_result_object_from_kiwi_response(cls, api_response):
        """
        Creates Response objects from JSON containing an individual itinerary from KIWI API flight search results
        :param api_response: JSON containing flight search results
        :return: Result object
        """

        result = cls(
            fly_from=Airport.objects.filter(iata_code=api_response['flyFrom']).first(),
            fly_to=Airport.objects.filter(iata_code=api_response['flyTo']).first(),
            departure_duration=timedelta(seconds=api_response['duration']['departure']),
            return_duration=timedelta(seconds=api_response['duration']['return']),
            departure_date=datetime.strptime(api_response['local_departure'], "%Y-%m-%dT%H:%M:%S.%fZ").date(),
            return_date=datetime.strptime(api_response['route'][-1]['local_departure'], "%Y-%m-%dT%H:%M:%S.%fZ").date(),        # TODO get actual date for first return flight
            departure_time=datetime.strptime(api_response['local_departure'], "%Y-%m-%dT%H:%M:%S.%fZ").time(),
            departure_arrival_time=datetime.strptime(api_response['local_arrival'], "%Y-%m-%dT%H:%M:%S.%fZ").time(),
            return_time=datetime.strptime(api_response['route'][-1]['local_departure'], "%Y-%m-%dT%H:%M:%S.%fZ").time(),        # TODO get actual date for first return flight
            return_arrival_time=datetime.strptime(api_response['route'][-1]['local_arrival'], "%Y-%m-%dT%H:%M:%S.%fZ").time(),
            has_airport_change=api_response['has_airport_change'],
            number_of_stops_departure=sum(1 for flight in api_response['route'] if flight['return'] == 0) - 1,
            number_of_stops_return=sum(1 for flight in api_response['route'] if flight['return'] == 1) - 1,
            price=api_response['price'],
            booking_token=api_response['booking_token'],
        )

        # TODO figure out how to add without creating database entries or how to delete data after session
        # for flight in api_response['data']['route']:
        #     result.flights.set(Flight.)
        #
        # for airline in api_response['airlines']:
        #     result.airlines.set(Airline.get_airline(airline))

        return result



class Subscription(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
