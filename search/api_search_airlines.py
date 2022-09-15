import requests

from django.http import HttpResponse
from .models import Airline



def get_airline_data_from_rapidapi():
    """
    Pulls all airports with IATA codes from API and creates new instances of
    all countries, cities and airports
    """
    api_endpoint = 'https://iata-and-icao-codes.p.rapidapi.com/airlines'
    headers = {
        "X-RapidAPI-Key": "8d22ba8fdcmshd22bde68fc3e5e9p15e8bdjsn98ccb2520125",
        "X-RapidAPI-Host": "iata-and-icao-codes.p.rapidapi.com"
    }
    errors = ""

    if not Airline.objects.all():
        response = requests.get(
            url=api_endpoint,
            headers=headers
        )
        response.raise_for_status()

        data = response.json()

        for airline in data:
            try:
                a = Airline(
                    iata_code=airline.get('iata_code'),
                    name=airline.get('name'),
                    logo=f"https://daisycon.io/images/airline/?width=350&height=100&color=ffffff&iata={airline.get('iata_code')}"
                )
                a.save()
            except Exception as ex:
                print(ex)
                errors += f"{ex}\n"

        print(f"Airline data added. \nErrors: \n{errors} ")

    print('Airline data already exists')
