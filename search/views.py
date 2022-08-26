import json

import requests
import environ

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime, timedelta

from .models import Country, City, Airport, Airline, Flight, Search
from viewer.models import Profile

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def get_airport_data_from_easypnr_api():
    '''
    Pulls all airports with IATA codes from API and creates new instances of all countries, cities and airports
    '''
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

        return HttpResponse('Airport data added')
    else:
        return HttpResponse('Airport data already exists')


def create_search_object(request) -> Search:
    '''
    Creates a search object from request.GET
    :param request:
    :return: Search object
    '''

    parameters = request.GET
    print(parameters)

    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
    else:
        user = None

    search = Search(
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
        locale=request.LANGUAGE_CODE,
    )
    return search


def create_query_for_kiwi_api(search) -> dict:
    '''
    Generate search query for KIWI api from a Search object
    :param search: Search object
    :return: dictionary containing search parameters
    '''

    query = {
        'fly_from': search.fly_from,  #
        'fly_to': search.fly_to,  #
        'date_from': (datetime.now().date() - timedelta(days=5)).strftime("%d/%m/%Y"),
        'date_to': (datetime.now().date() + timedelta(days=10)).strftime("%d/%m/%Y"),
        'flight_type': search.flight_type,
        'adults': search.adults,
        'children': search.children,
        'infants': search.infants,
        'selected_cabins': search.selected_cabins,
        'curr': search.curr,
        'locale': search.locale,
        'limit': search.limit
    }
    #
    if search.search_type == "duration":
        query['nights_in_dst_from'] = search.nights_in_dst_from
        query['nights_in_dst_to'] = search.nights_in_dst_to

    if search.flight_type == "round":
        query['return_from'] = (datetime.now().date() - timedelta(days=search.flexible)).strftime("%d/%m/%Y")
        query['return_to'] = (datetime.now().date() + timedelta(days=100)).strftime("%d/%m/%Y")

    print(f"duration '{search.max_fly_duration}'")
    if not search.max_fly_duration != 0:
        query['max_fly_duration'] = search.max_fly_duration

    if search.max_stopovers != '':
        query['max_stopovers'] = search.max_stopovers
    print(query)
    return query


def search_from_kiwi_api(search):
    '''
    Search for flights using KIWI api.
    KIWI search query is generated using the passed Search object.
    :param search: Search object
    :return: API response
    '''

    endpoint_search = "https://tequila-api.kiwi.com/v2/search"
    endpoint_city_search = "https://tequila-api.kiwi.com/locations/query"

    headers = {
        "accept": "application/json",
        "apikey": f'{env("KIWI_TEQUILA_API_KEY")}'
    }

    query = create_query_for_kiwi_api(search)

    response = requests.get(url=endpoint_search, headers=headers, params=query)

    response.raise_for_status()
    return response.json()


def flight_search(request) -> HttpResponse:
    '''
    Searches for flights based on request parameters.

    From request parameters, a Search object is created using a function.
    This object is passed to API search function that returns a Result object

    :param request:
    :return: HTTPResponse
    '''
    search = create_search_object(request=request)

    response = search_from_kiwi_api(search)

    print(response)

    return HttpResponse(search)
