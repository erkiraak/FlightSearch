from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from search.models import Search, Airport


class DateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(forms.ModelForm):

    def clean_fly_from(self):
        data = self.cleaned_data['fly_from']
        airport = Airport.objects.filter(
            Q(iata_code__icontains=data) |
            Q(name__icontains=data) |
            Q(city__icontains=data) |
            Q(city_code__icontains=data) |
            Q(country__icontains=data) |
            Q(country_code__icontains=data)
        )

        if airport.exists():
            return airport.first().iata_code

        else:
            raise ValidationError("Please enter a valid destination")

    def clean_fly_to(self):
        data = self.cleaned_data['fly_to']
        airport = Airport.objects.filter(
            Q(iata_code__icontains=data) |
            Q(name__icontains=data) |
            Q(city__icontains=data) |
            Q(city_code__icontains=data) |
            Q(country__icontains=data) |
            Q(country_code__icontains=data)
        )

        if airport.exists():
            return airport.first().iata_code

        else:
            raise ValidationError("Please enter a valid destination")

    def clean_return_date(self):
        departure_date = self.cleaned_data['departure_date']
        return_date = self.cleaned_data['return_date']
        print(departure_date)
        print(return_date)
        if departure_date > return_date:
            raise ValidationError("Return date cannot be before departure date")

        else:
            return return_date

    class Meta:
        model = Search
        exclude = ('user', 'locale', 'limit')
        widgets = {
            'departure_date': DateInput(),
            'return_date': DateInput(),
        }

        help_texts = {
            'fly_from': 'Enter full city name.',
            'fly_to': 'Enter full city name.',
        }
        labels = {
            'curr': 'Currency:',
        }
