import requests
import environ

from django.http import HttpResponse

from .models import Airport

env = environ.Env(
    DEBUG=(bool, False)
)


def get_airport_data_from_easypnr_api():
    """
    Pulls all airports with IATA codes from API and creates new instances of
    all countries, cities and airports
    """
    api_endpoint = 'http://api.easypnr.com/v4/airports'
    api_key = env('EASYPNR_API_KEY')
    headers = {'X-Api-Key': api_key}

    if not Airport.objects.all():
        response = requests.get(
            url=api_endpoint,
            headers=headers
        )
        response.raise_for_status()

        data = response.json()
        for airport in data:
            try:
                Airport.objects.create(
                    iata_code=airport['iataCode'],
                    name=airport['locationName'],
                    city=airport['location'],
                    country=airport['country']
                )
            except Exception as ex:
                print(ex)

    else:
        message = 'Airport data already exists'

    return HttpResponse(message)
