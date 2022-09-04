import requests
import environ

from datetime import timedelta
from .models import Search


def create_query_for_kiwi_api(search: Search) -> dict:
    """
    Generate search query for KIWI api from a Search object
    :param search: Search object
    :return: dictionary containing search parameters
    """
    # TODO create proper IATA search
    query = {
        'fly_from': search.fly_from.upper(),
        'fly_to': search.fly_to.upper(),
        'date_from': (
                search.departure_date
                - timedelta(days=search.flexible)
        ).strftime("%d/%m/%Y"),
        'date_to': (
                search.departure_date
                + timedelta(days=search.flexible)
        ).strftime("%d/%m/%Y"),
        'flight_type': search.flight_type,
        'adults': search.adults,
        'children': search.children,
        'infants': search.infants,
        'selected_cabins': search.selected_cabins,
        'curr': search.curr,
        'locale': search.locale,
        'limit': search.limit
    }

    if search.search_type == "duration":
        query['nights_in_dst_from'] = search.nights_in_dst_from
        query['nights_in_dst_to'] = search.nights_in_dst_to

    if search.flight_type == "round":
        query['return_from'] = (
                search.return_date - timedelta(days=search.flexible)
        ).strftime("%d/%m/%Y")

        query['return_to'] = (
                search.return_date + timedelta(days=search.flexible)
        ).strftime("%d/%m/%Y")

    if not search.max_fly_duration != '':
        query['max_fly_duration'] = search.max_fly_duration

    if search.max_stopovers not in ['', None]:
        query['max_stopovers'] = search.max_stopovers

    return query


def search_from_kiwi_api(search: Search) -> dict or None:
    """
    Search for flights using KIWI api.
    KIWI search query is generated using the passed Search object.
    :param search: Search object
    :return: API api_response
    """

    endpoint_search = "https://tequila-api.kiwi.com/v2/search"
    # endpoint_city_search = "https://tequila-api.kiwi.com/locations/query"

    headers = {
        "accept": "application/json",
        "apikey": f'{environ.Env(DEBUG=(bool, False))("KIWI_TEQUILA_API_KEY")}'
    }

    query = create_query_for_kiwi_api(search)
    try:
        api_response = requests.get(
            url=endpoint_search,
            headers=headers,
            params=query
        )
        api_response.raise_for_status()

    except requests.exceptions.HTTPError:
        return None

    return api_response.json()
