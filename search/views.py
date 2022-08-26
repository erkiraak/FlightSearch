import requests
import environ

from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime, timedelta

from .models import Country, City, Airport, Airline, Flight, Search, Result
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


def create_query_for_kiwi_api(search) -> dict:
    '''
    Generate search query for KIWI api from a Search object
    :param search: Search object
    :return: dictionary containing search parameters
    '''

    query = {
        'fly_from': search.fly_from,  # TODO create proper IATA search
        'fly_to': search.fly_to,  # TODO create proper IATA search
        'date_from': (datetime.strptime(search.departure_date, '%Y-%m-%d') -
                      timedelta(days=search.flexible)).strftime("%d/%m/%Y"),
        'date_to': (datetime.strptime(search.departure_date, '%Y-%m-%d') +
                    timedelta(days=search.flexible)).strftime("%d/%m/%Y"),
        'flight_type': search.flight_type,
        'adults': search.adults,
        'children': search.children,
        'infants': search.infants,
        'selected_cabins': search.selected_cabins,  # TODO add mixed cabin option
        'curr': search.curr,
        'locale': search.locale,
        'limit': search.limit
    }

    if search.search_type == "duration":
        query['nights_in_dst_from'] = search.nights_in_dst_from
        query['nights_in_dst_to'] = search.nights_in_dst_to

    if search.flight_type == "round":
        query['return_from'] = (datetime.strptime(search.return_date, '%Y-%m-%d') -
                                timedelta(days=search.flexible)).strftime("%d/%m/%Y")
        query['return_to'] = (datetime.strptime(search.return_date, '%Y-%m-%d') +
                              timedelta(days=search.flexible)).strftime("%d/%m/%Y")

    if not search.max_fly_duration != '':
        query['max_fly_duration'] = search.max_fly_duration

    if search.max_stopovers != '':
        query['max_stopovers'] = search.max_stopovers

    return query


def search_from_kiwi_api(search):
    '''
    Search for flights using KIWI api.
    KIWI search query is generated using the passed Search object.
    :param search: Search object
    :return: API api_response
    '''

    endpoint_search = "https://tequila-api.kiwi.com/v2/search"
    endpoint_city_search = "https://tequila-api.kiwi.com/locations/query"

    headers = {
        "accept": "application/json",
        "apikey": f'{env("KIWI_TEQUILA_API_KEY")}'
    }

    query = create_query_for_kiwi_api(search)

    try:
        api_response = requests.get(url=endpoint_search, headers=headers, params=query)
        api_response.raise_for_status()
    except Exception as ex:
        print(ex)
        return ex

    # TODO implement api response check and error reporting

    return api_response.json()


def flight_search(request) -> HttpResponse:
    '''
    Searches for flights based on request parameters.

    From request parameters, a Search object is created using a function.
    This object is passed to API search function that returns a Result object

    :param request:
    :return: HTTPResponse
    '''
    search = Search.create_search_object_from_request(request=request)

    api_response = search_from_kiwi_api(search)

    results = [Result.create_result_object_from_kiwi_response(result) for result in api_response['data']]

    context = {
        'itineraries': results
    }

    return render(request, template_name='search/results.html', context=context)
