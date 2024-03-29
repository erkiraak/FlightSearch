from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView)

from search.models import Search
from .models import Subscription


# TODO OPTIONAL change CreateSubscription type to avoid POST issues
class CreateSubscription(LoginRequiredMixin, CreateView):
    model = Subscription
    success_url = reverse_lazy('list_subscription')
    fields = ('price_to', 'curr', 'email')
    object = None

    def get_form(self, form_class=None):
        form = super(CreateSubscription, self).get_form(form_class)
        form.fields['price_to'].required = True
        form.fields['email'].required = True
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.search = Search.objects.get(id=self.kwargs['pk'])
        self.object.search.price_to = self.object.price_to
        self.object.search.curr = self.object.curr
        self.object.search.save()
        self.object.save()
        return super().form_valid(form)


class ListSubscription(LoginRequiredMixin, ListView):
    template_name = 'list_subscription.html'
    model = Subscription
    context_object_name = 'subscription'

    def get_queryset(self):
        subscriptions = Subscription.objects.filter(user=self.request.user)
        return subscriptions


class UpdateSubscription(LoginRequiredMixin, UpdateView):
    model = Subscription
    success_url = reverse_lazy('list_subscription')
    fields = ('price_to', 'curr', 'email')
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.search.price_to = self.object.price_to
        self.object.search.curr = self.object.curr
        self.object.search.email = self.object.email
        self.object.search.save()
        return super().form_valid(form)


class DeleteSubscription(LoginRequiredMixin, DeleteView):
    model = Subscription
    success_url = reverse_lazy('list_subscription')
    context_object_name = 'subscription'


class DeleteAllSubscription(LoginRequiredMixin, DeleteView):
    model = Subscription
    success_url = reverse_lazy('index')
    context_object_name = 'subscription'

    def get_queryset(self):
        subscriptions = Subscription.objects.filter(user=self.request.user)
        return subscriptions

    def get_object(self, queryset=None):
        return self.get_queryset()

