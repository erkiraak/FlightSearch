from constants import CABINS, CURRENCIES, STOPOVERS, FLIGHT_TYPE, SEARCH_TYPE
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models


class Airport(models.Model):
    iata_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# TODO add airline API call
class Airline(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=2)
    logo = models.ImageField(upload_to='airline_logos', blank=True)

    @classmethod
    def add_airline_by_code(cls, code):
        airline = cls(code=code)
        airline.save()
        return airline

    @classmethod
    def get_airline(cls, code):
        try:
            airline = cls.objects.get(code=code)
        except models.ObjectDoesNotExist:
            airline = cls.add_airline_by_code(code)

        return airline


class Flight(models.Model):
    search = models.ForeignKey('Search', on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
    flight_no = models.CharField(max_length=10)
    fly_from = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='flight_fly_from',
    )
    fly_to = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='flight_fly_to'
    )
    local_arrival = models.DateTimeField()
    local_departure = models.DateTimeField()
    fare_category = models.CharField(max_length=1)
    segment_no = models.IntegerField()
    return_flight = models.BooleanField()

    # TODO implement flight creation
    @classmethod
    def create_flight_object_from_kiwi_response(cls, api_response):
        pass


class Search(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    search_type = models.CharField(
        max_length=10,
        default='strict',
        choices=SEARCH_TYPE
    )
    flight_type = models.CharField(
        max_length=10,
        default='round',
        choices=FLIGHT_TYPE
    )
    fly_from = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='search_fly_from',
        blank=True,
        null=True
    )
    fly_to = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='search_fly_to',
        blank=True,
        null=True
    )
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    flexible = models.BooleanField(default=False)
    nights_in_dst_from = models.PositiveIntegerField(default=7)
    nights_in_dst_to = models.PositiveIntegerField(default=14)
    max_fly_duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=None
    )
    adults = models.PositiveIntegerField(blank=True, default=1)
    children = models.PositiveIntegerField(blank=True, default=0)
    infants = models.PositiveIntegerField(blank=True, default=0)
    selected_cabins = models.CharField(
        max_length=1,
        choices=CABINS,
        default='M')
    curr = models.CharField(max_length=3, choices=CURRENCIES, default='EUR')
    price_from = models.IntegerField(blank=True, null=True)
    price_to = models.IntegerField(blank=True, null=True)
    max_stopovers = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        choices=STOPOVERS
    )
    limit = models.IntegerField(default=1)
    locale = models.CharField(max_length=5, default='en')

    def __str__(self):
        return f'{self.fly_from.name} - {self.fly_to.name}'

    def save(self, *args, **kwargs):
        if self.user:
            total_objects = Search.objects.filter(user=self.user).count()

            if total_objects >= 25:
                self.delete_search(24)

        super().save(*args, **kwargs)

    def delete_search(self, nr_remaining):
        pk = Search.objects.filter(user=self.user
                                   ).order_by('-id'
                                              ).values('pk')[nr_remaining:]

        for key in pk:
            try:
                Search.objects.get(pk=key['pk']).delete()
            except models.ProtectedError as e:
                print(e)

    @classmethod
    def create_search_object_from_request(cls, cleaned_data, user):
        """
        Creates a search object from cleaned data
        :param user: User object
        :param cleaned_data: dictionary with cleaned data
        :return: Search object
        """

        if not user.is_authenticated:
            user = None

        search = cls(
            user=user,
            flight_type=cleaned_data.get('flight_type'),
            search_type=cleaned_data.get('search_type'),
            fly_from=cleaned_data.get('fly_from'),
            fly_to=cleaned_data.get('fly_to'),
            departure_date=cleaned_data.get('departure_date'),
            return_date=cleaned_data.get('return_date'),
            flexible=cleaned_data.get('flexible'),
            nights_in_dst_from=cleaned_data.get('nights_in_dst_from'),
            nights_in_dst_to=cleaned_data.get('nights_in_dst_to'),
            max_fly_duration=cleaned_data.get('max_fly_duration'),
            max_stopovers=cleaned_data.get('max_stopovers'),
            adults=cleaned_data.get('adults'),
            children=cleaned_data.get('children'),
            infants=cleaned_data.get('infants'),
            selected_cabins=cleaned_data.get('selected_cabins'),
            curr=cleaned_data.get('curr'),
            price_from=cleaned_data.get('price_from'),
            price_to=cleaned_data.get('price_to'),
            limit=cleaned_data.get('limit'),
        )
        search.save()
        return search


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    airlines = models.ManyToManyField(Airline)
    fly_from = models.ForeignKey(
        Airport,
        related_name='result_fly_from',
        on_delete=models.CASCADE
    )
    fly_to = models.ForeignKey(
        Airport,
        related_name='result_fly_to',
        on_delete=models.CASCADE
    )
    departure_duration = models.DurationField()
    return_duration = models.DurationField()
    departure_date = models.DateField()
    return_date = models.DateField()
    departure_time = models.TimeField()
    departure_arrival_time = models.TimeField()
    return_time = models.TimeField()
    return_arrival_time = models.TimeField()
    connecting_airport_departure = models.ManyToManyField(
        Airport,
        related_name='connecting_airport_departure'
    )
    connecting_airport_return = models.ManyToManyField(
        Airport,
        related_name='connecting_airport_return'
    )
    has_airport_change = models.BooleanField()
    number_of_stops_departure = models.IntegerField()
    number_of_stops_return = models.IntegerField()
    price = models.IntegerField()
    flights = models.ManyToManyField(Flight)
    booking_token = models.CharField(max_length=1000)

    @classmethod
    def create_result_object_from_kiwi_response(cls, api_response, search_id):
        """
        Creates Response objects from JSON containing an individual itinerary
        from KIWI API flight search results
        :param search_id: PK of used Search object
        :param api_response: JSON containing flight search results
        :return: Result object
        """
        result = cls(
            search=Search.objects.filter(id=search_id).first(),
            fly_from=Airport.objects.filter(
                iata_code=api_response['flyFrom']
            ).first(),
            fly_to=Airport.objects.filter(
                iata_code=api_response['flyTo']
            ).first(),
            departure_duration=timedelta(
                seconds=api_response['duration']['departure']
            ),
            return_duration=timedelta(
                seconds=api_response['duration']['return']
            ),
            departure_date=datetime.strptime(
                api_response['local_departure'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date(),
            return_date=datetime.strptime(
                api_response['route'][-1]['local_departure'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date(),
            # TODO get actual date for first return flight
            departure_time=datetime.strptime(
                api_response['local_departure'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            departure_arrival_time=datetime.strptime(
                api_response['local_arrival'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            return_time=datetime.strptime(
                api_response['route'][-1]['local_departure'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            # TODO get actual date for first return flight
            return_arrival_time=datetime.strptime(
                api_response['route'][-1]['local_arrival'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            has_airport_change=api_response['has_airport_change'],
            number_of_stops_departure=sum(
                1 for flight in api_response['route'] if
                flight['return'] == 0
            ) - 1,
            number_of_stops_return=sum(
                1 for flight in api_response['route'] if
                flight['return'] == 1
            ) - 1,
            price=api_response['price'],
            booking_token=api_response['booking_token'],
        )

        # for flight in api_response['data']['route']:
        #     result.flights.set(Flight.)
        #
        # for airline in api_response['airlines']:
        #     result.airlines.set(Airline.get_airline(airline))
        result.save()
        return result
