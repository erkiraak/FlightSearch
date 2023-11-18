import environ
import requests

from datetime import timedelta
from .models import Search

KIWI_API_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
KIWI_API_KEY = environ.Env(DEBUG=(bool, False))("KIWI_TEQUILA_API_KEY")

def search_from_kiwi_api(search: Search) -> dict or None:
    """
    Search for flights using KIWI api.
    KIWI search query is generated using the passed Search object.
    :param search: Search object
    :return: API api_response
    """

    headers = {
        "accept": "application/json",
        "apikey": KIWI_API_KEY
    }
    query = create_query_for_kiwi_api(search)
    try:
        api_response = requests.get(
            url=KIWI_API_ENDPOINT,
            headers=headers,
            params=query
        )
        api_response.raise_for_status()
        return api_response.json()

    except requests.exceptions.HTTPError:
        return None


def create_query_for_kiwi_api(search: Search) -> dict:
    """
    Generate search query for KIWI api from a Search object
    :param search: Search object
    :return: dictionary containing search parameters
    """
    # TODO: move to model
    flexible = 0
    if search.flexible:
        flexible = 3

    query = {
        'fly_from': search.fly_from.iata_code,
        'fly_to': search.fly_to.iata_code,
        'date_from': (search.departure_date - timedelta(days=flexible)).strftime("%d/%m/%Y"),
        'date_to': (search.departure_date + timedelta(days=flexible)).strftime("%d/%m/%Y"),
        'flight_type': search.flight_type,
        'adults': search.adults,
        'children': search.children,
        'infants': search.infants,
        'selected_cabins': search.selected_cabins,
        'curr': search.curr,
        'locale': search.locale,
        'limit': search.limit
    }

    if search.flight_type == "round":
        query['return_from'] = (search.return_date - timedelta(days=flexible)).strftime("%d/%m/%Y")
        query['return_to'] = (search.return_date + timedelta(days=flexible)).strftime("%d/%m/%Y")

    if search.search_type == "duration" and search.flight_type == "round":
        query['date_to'] = (search.return_date - timedelta(days=search.nights_in_dst_from)).strftime("%d/%m/%Y")
        query['return_from'] = (search.departure_date + timedelta(days=search.nights_in_dst_from)).strftime("%d/%m/%Y")
        query['nights_in_dst_from'] = search.nights_in_dst_from
        query['nights_in_dst_to'] = search.nights_in_dst_to

    if not search.max_fly_duration != '':
        query['max_fly_duration'] = search.max_fly_duration

    if search.max_stopovers not in ['', None]:
        query['max_stopovers'] = search.max_stopovers

    if search.price_to:
        query['price_to'] = search.price_to

    if search.price_from:
        query['price_from'] = search.price_from

    return query

