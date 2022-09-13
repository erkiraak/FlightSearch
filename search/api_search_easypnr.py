import environ
import requests

from django.http import HttpResponse
from .models import Airport


def get_airport_data_from_easypnr_api():
    """
    Pulls all airports with IATA codes from API and creates new instances of
    all countries, cities and airports
    """
    api_endpoint = 'http://api.easypnr.com/v4/airports'
    api_key = environ.Env(DEBUG=(bool, False))('EASYPNR_API_KEY')
    headers = {'X-Api-Key': api_key}
    errors = ""

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
                    name=airport.get('locationName'),
                    city=airport.get('location'),
                    country=airport.get('country')
                )
            except Exception as ex:
                errors += f"{ex}\n"

        return HttpResponse(f"Airport data added. \nErrors: \n{errors} ")

    return HttpResponse('Airport data already exists')
