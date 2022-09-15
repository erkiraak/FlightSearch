from django import template
from ..models import Airline, Airport

register = template.Library()


@register.filter(name='listofnames')
def listofnames(qs):
    string = ''
    if isinstance(qs.first(), Airline):
        for airline in qs:
            string += f"{airline.name}, "
    elif isinstance(qs.first(), Airport):
        for airport in qs:
            string += f"{airport.iata_code}, "

    return string[:-2]

