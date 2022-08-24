import requests
import environ

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from .models import Country, City, Airport, Airline, Flight, Search
from viewer.models import Profile

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def get_airport_data_from_easypnr_api():
    """
    Pulls all airports with IATA codes from API and creates new instances of all countries, cities and airports
    """
    api_endpoint = 'http://api.easypnr.com/v4/airports'
    api_key = env('EASYPNR_API_KEY')
    headers = {'X-Api-Key': api_key}

    if not Airport.objects.all():
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()

        data = response.json()
        for airport in data:
            try:
                Country.objects.create(name=airport['country'], code='')

                City.objects.create(name=airport['location'],
                                code='',
                                country=Country.objects.get(name=airport['country']))


                Airport.objects.create(iata_code=airport['iataCode'],
                                       city=City.objects.get(name=airport['location']),
                                       country=Country.objects.get(name=airport['country']))
            except Exception as ex:
                print(ex)

        return HttpResponse("Airport data added")
    else:
        return HttpResponse('Airport data already exists')



def flight_search(request)->HttpResponse:
    """
    Searches for flights based on request parameters.

    From request parameters, a Search object is created. This object is passed to API search function that returns a
    Result object

    :param request:
    :return: HTTPResponse
    """
    parameters = request.GET

    search = Search(
        user=Profile.objects.get(user=request.user),
        flight_type=parameters.get('flight_type'),
        search_type=parameters.get('search_type'),
        fly_from=parameters.get('fly_from'),
        fly_to=parameters.get('fly_to'),
        date_from=parameters.get('date_from'),
        date_to=parameters.get('date_to'),
        return_from=parameters.get('return_from'),
        return_to=parameters.get('return_to'),
        nights_in_dst_from=parameters.get('nights_in_dst_from'),
        nights_in_dst_to=parameters.get('nights_in_dst_to'),
        max_fly_duration=parameters.get('max_fly_duration'),
        max_stopovers=parameters.get('max_stopovers'),
        adults=parameters.get('adults'),
        children=parameters.get('children'),
        infants=parameters.get('infants'),
        selected_cabins=parameters.get('selected_cabins'),
        mix_with_cabins=parameters.get('mix_with_cabins'),
        curr=parameters.get('curr'),
        price_to=parameters.get('price_to'),
    )

    print(parameters.get('whaat'))
    print(request.user)
    print(parameters)

    return HttpResponse(parameters)

