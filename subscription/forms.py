from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from subscription.models import Subscription


class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(initial={'email': 'erjki@maial.ee'})

    class Meta:
        model = Subscription
        exclude = ('user', 'search')
        # widgets = {
        #     'departure_date': DateInput(),
        # }
        #
        # help_texts = {
        #     'fly_from': 'Enter full city name.',
        # }
        labels = {
            'curr': 'Currency:',
        }

        def validate(self):
            pass

