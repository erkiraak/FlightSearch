import environ
import requests
import logging

from .models import Airline

RAPIDAPI_ENDPOINT = 'https://iata-and-icao-codes.p.rapidapi.com/airlines'
RAPIDAPI_KEY = environ.Env(DEBUG=(bool, False))('RAPIDAPI_API_KEY')

def get_airline_data_from_rapidapi() -> None:
    """
    Pulls all airports with IATA codes from API and creates new instances of
    all countries, cities and airports.
    If any airlines present in database the function exits, partially adding data not supported.
    """

    if Airline.objects.all():
        logging.info('Airline data already exists')
        return

    logging.info("Adding airlines")

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "iata-and-icao-codes.p.rapidapi.com"
    }
    response = requests.get(
        url=RAPIDAPI_ENDPOINT,
        headers=headers
    )
    response.raise_for_status()
    airline_data = response.json()

    for airline in airline_data:
        try:
            Airline.objects.create(
                iata_code=airline.get('iata_code'),
                name=airline.get('name'),
                logo=f"https://daisycon.io/images/airline/?width=350&height=100&color=ffffff&iata="
                     f"{airline.get('iata_code')}"
            )
        except Exception as exception:
            logging.warning(exception)

    logging.info(f"Airline data added")

