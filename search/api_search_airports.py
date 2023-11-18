import environ
import requests
import logging

from .models import Airport

EASYPNR_API_ENDPOINT = 'http://api.easypnr.com/v4/airports'
EASYPNR_API_KEY = environ.Env(DEBUG=(bool, False))('EASYPNR_API_KEY')

def get_airport_data_from_easypnr_api():
    """
    Pulls all airports with IATA codes from API and creates new instances of
    all countries, cities and airports
    If any airports present in database the function exits, partially adding data not supported.

    """
    if Airport.objects.all():
        logging.info('Airport data already exists')
        return

    logging.info("Adding airports")

    headers = {'X-Api-Key': EASYPNR_API_KEY}
    response = requests.get(
        url=EASYPNR_API_ENDPOINT,
        headers=headers
    )
    response.raise_for_status()

    airport_data = response.json()
    for airport in airport_data:
        try:
            Airport.objects.create(
                iata_code=airport['iataCode'],
                name=airport.get('locationName'),
                city=airport.get('location'),
                country=airport.get('country')
            )

        except Exception as exception:
            logging.warning(exception)

    logging.info(f"Airport data added")
