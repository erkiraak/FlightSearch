from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from constants import CABINS, CURRENCIES, FLIGHT_TYPE, SEARCH_TYPE


class Airport(models.Model):
    iata_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city}({self.iata_code})'


class Airline(models.Model):
    iata_code = models.CharField(max_length=3)
    name = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='./media/airline_logos', blank=True)

    @classmethod
    def add_airline_by_code(cls, code):
        a = cls(
            iata_code=code,
            name=code,
            logo=f"https://daisycon.io/images/airline/"
                 f"?width=350&height=100&color=ffffff&iata={code}"
        )
        a.save()
        return a
    # TODO OPTIONAL implement airline search api
    @classmethod
    def get_or_create_airline(cls, code):
        try:
            airline = cls.objects.get(iata_code=code)
        except models.ObjectDoesNotExist:
            airline = cls.add_airline_by_code(code)

        return airline


class Flight(models.Model):
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
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
    departure_date = models.DateField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    departure_arrival_time = models.TimeField(null=True, blank=True)
    fare_category = models.CharField(max_length=1)

    @classmethod
    def create_flight_object_from_kiwi_response(cls, api_response, result_id):
        """
        Creates Flight objects from JSON containing an individual flight
        from KIWI API flight search results
        :param result_id: PK of used Result object
        :param api_response: JSON containing flight data
        :return: Result object
        """
        flight = cls(
            result=Result.objects.get(id=result_id),
            airline=Airline.get_or_create_airline(
                code=api_response.get('airline')
            ),
            flight_no=api_response.get('flight_no'),
            fly_from=Airport.objects.get(
                iata_code=api_response.get('flyFrom')
            ),
            fly_to=Airport.objects.get(
                iata_code=api_response.get('flyTo')
            ),
            fare_category=api_response.get('fare_category'),
            departure_date=datetime.strptime(
                api_response.get('local_departure'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date(),
            departure_time=datetime.strptime(
                api_response.get('local_departure'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            departure_arrival_time=datetime.strptime(
                api_response.get('local_arrival'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
        )
        flight.save()
        return flight


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
    departure_date = models.DateField(
        default=datetime.now().date() + timedelta(14)
    )
    return_date = models.DateField(
        default=datetime.now().date() + timedelta(21),
        blank=True,
        null=True
    )
    flexible = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    nights_in_dst_from = models.PositiveIntegerField(
        default=7,
        null=True,
        blank=True)
    nights_in_dst_to = models.PositiveIntegerField(
        default=14,
        null=True,
        blank=True)
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
    )
    limit = models.IntegerField(default=10)
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
            except models.ProtectedError:
                pass

    # TODO optional add error handling
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
            # limit=cleaned_data.get('limit'),
        )
        search.save()
        return search


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
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
    return_duration = models.DurationField(null=True, blank=True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_arrival_time = models.TimeField()
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    return_arrival_time = models.TimeField(null=True, blank=True)
    connecting_airport_departure = models.ManyToManyField(
        Airport,
        related_name='connecting_airport_departure'
    )
    connecting_airport_return = models.ManyToManyField(
        Airport,
        related_name='connecting_airport_return',
    )
    has_airport_change = models.BooleanField()
    number_of_stops_departure = models.IntegerField()
    number_of_stops_return = models.IntegerField(null=True, blank=True)
    price = models.IntegerField()
    departure_flights = models.ManyToManyField(
        Flight,
        related_name='departure_flights'
    )
    departure_airlines = models.ManyToManyField(
        Airline,
        related_name='departure_airlines'
    )
    return_flights = models.ManyToManyField(
        Flight,
        related_name='return_flights',
    )
    return_airlines = models.ManyToManyField(
        Airline,
        related_name='return_airlines'
    )
    booking_token = models.CharField(max_length=1000)

    # TODO optional add error handling
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
            search=Search.objects.get(id=search_id),
            fly_from=Airport.objects.get(
                iata_code=api_response.get('flyFrom')
            ),
            fly_to=Airport.objects.get(
                iata_code=api_response.get('flyTo')
            ),
            departure_duration=timedelta(
                seconds=api_response.get('duration').get('departure')
            ),
            departure_date=datetime.strptime(
                api_response.get('local_departure'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date(),
            departure_time=datetime.strptime(
                api_response.get('local_departure'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            departure_arrival_time=datetime.strptime(
                api_response.get('local_arrival'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time(),
            has_airport_change=api_response.get('has_airport_change'),
            number_of_stops_departure=sum(
                1 for flight in api_response.get('route') if
                flight['return'] == 0
            ) - 1,
            price=api_response.get('price'),
            booking_token=api_response.get('booking_token'),
        )

        if api_response.get('duration').get('return') != 0:
            result.return_duration = timedelta(
                seconds=api_response.get('duration').get('return')
            )
            result.return_date = datetime.strptime(
                cls.get_first_return_flight(api_response.get('route')),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date()
            result.return_time = datetime.strptime(
                cls.get_first_return_flight(api_response.get('route')),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time()
            result.return_arrival_time = datetime.strptime(
                api_response.get('route')[-1].get('local_arrival'),
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).time()
            result.number_of_stops_return = sum(
                1 for flight in api_response['route'] if
                flight['return'] == 1
            ) - 1
        result.save()

        for flight in api_response.get('route'):
            flight_object = Flight.create_flight_object_from_kiwi_response(
                api_response=flight,
                result_id=result.id
            )
            if flight.get('return') == 0:
                result.departure_flights.add(flight_object)
                result.departure_airlines.add(flight_object.airline)
                if flight_object.fly_to not in [result.fly_to, result.fly_from]:
                    result.connecting_airport_departure.add(
                        flight_object.fly_to
                    )
            else:
                result.return_flights.add(flight_object)
                result.return_airlines.add(flight_object.airline)
                if flight_object.fly_to not in [result.fly_to, result.fly_from]:
                    result.connecting_airport_return.add(flight_object.fly_to)

        return result

    @staticmethod
    def get_first_return_flight(route):
        for flight in route:
            if flight.get('return') == 1:
                return flight.get('local_departure')
