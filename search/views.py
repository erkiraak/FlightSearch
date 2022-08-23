import requests
import environ
from functools import lru_cache

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from .models import Country, City, Airport, Airline, Flight, Search

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def get_airport_data_from_easypnr_api(request):
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
