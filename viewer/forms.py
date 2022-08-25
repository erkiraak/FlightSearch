from django import forms
from django.forms import ModelForm
from search.models import Search


class DateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = '__all__'
        widgets = {
            'departure_date': DateInput(),
            'return_date': DateInput(),
        }
