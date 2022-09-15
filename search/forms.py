import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import TextField

from search.models import Search


class DateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(forms.ModelForm):
    fly_from = TextField()
    fly_to = TextField()

    class Meta:
        model = Search
        exclude = ('user', 'locale', 'limit')
        widgets = {
            'fly_from': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'required': 'required'
                }),
            'fly_to': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'required': 'required'
                }),
            'search_type': forms.Select(attrs={'class': "form-select"}),
            'flight_type': forms.Select(attrs={'class': "form-select"}),
            'curr': forms.Select(attrs={'class': "form-select"}),
            'selected_cabins': forms.Select(attrs={'class': "form-select"}),
            'departure_date': DateInput(attrs={'class': "form-control"}),
            'return_date': DateInput(
                attrs={
                    'class': "form-control",
                    'required': 'required'
                }),
            'nights_in_dst_from': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 1,
                    'max': 90,
                    # 'disabled': True,
                }),
            'nights_in_dst_to': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 1,
                    'max': 90,
                    # 'disabled': True,
                }),
            'flexible': forms.CheckboxInput(
                attrs={'class': "form-check-input"}),
            'adults': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                    'max': 10,
                }),
            'children': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                    'max': 10,
                }),
            'infants': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                    'max': 10,
                }),
            'max_fly_duration': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 1,
                    'max': 96,
                }),
            'max_stopovers': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                    'max': 5,
                }),
            'price_from': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                    'min-width': 320
                }),
            'price_to': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': 0,
                }),
        }

        help_texts = {
            'fly_from': 'Enter full city name.',
            'fly_to': 'Enter full city name.',
        }
        labels = {
            'curr': 'Currency:',
            'selected_cabins': 'Travel class',
            'search_type': 'Search',
            'flight_type': 'Flight',
            'flexible': 'Flexible dates (±3 days)',
            'nights_in_dst_from': 'From',
            'nights_in_dst_to': 'to',
            'max_fly_duration': 'Duration up to',
            'max_stopovers': 'Connections up to',
            'price_from': 'From',
            'price_to': 'to',
            'adults': 'Adults ',
            'infants': 'Infants ',
            'fly_from': 'Origin ',
            'fly_to': 'Destination ',
        }

    def clean_fly_from(self):
        fly_from = self.cleaned_data['fly_from']
        if fly_from is None:
            raise ValidationError("Please enter a valid origin")
        else:
            return fly_from

    def clean_fly_to(self):
        fly_to = self.cleaned_data['fly_to']
        if fly_to is None:
            raise ValidationError("Please enter a valid destination")
        else:
            return fly_to

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')
        today = datetime.datetime.now().date()
        if today > departure_date:
            raise ValidationError("Departure date cannot be in the past")
        else:
            return departure_date

    def clean_return_date(self):
        if self.cleaned_data.get('flight_type') == 'round':
            departure_date = self.cleaned_data.get('departure_date')
            return_date = self.cleaned_data.get('return_date')
            today = datetime.datetime.now().date()
            if today > return_date:
                raise ValidationError("Return date cannot be in the past")

            if departure_date and departure_date > return_date:
                raise ValidationError("Return date cannot be before departure date")
            else:
                return return_date

        return None
