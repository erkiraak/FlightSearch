from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ObjectDoesNotExist, Q, ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from .api_search_flights import search_from_kiwi_api
from .forms import SearchForm
from .models import Search, Result, Airport


def get_airport(search):
    try:
        iata = search[-4:-1]
        city = search[:-5]

        airport = Airport.objects.get(
            (Q(iata_code=iata) &
             Q(city=city)) |
            Q(iata_code=search.upper())
        )
    except (ObjectDoesNotExist, IndexError):
        airport = None

    return airport


def search_view(request):
    form = SearchForm(None)
    template = 'index.html'
    context = {
        'form': form,
    }

    if 'term' in request.GET:

        qs = Airport.objects.filter(
            name__icontains=request.GET.get('term'))[:10]

        names = []

        for airport in qs:
            names.append(f'{airport.city}({airport.iata_code})')
        return JsonResponse(names, safe=False)

    if request.method == 'POST':

        try:
            destination = request.POST['fly_from']
        except IndexError:
            destination = None

        if destination and not isinstance(destination, Airport):
            post_copy = request.POST.copy()
            post_copy['fly_from'] = get_airport(post_copy['fly_from'])
            post_copy['fly_to'] = get_airport(post_copy['fly_to'])
            form = SearchForm(post_copy)

        else:
            form = SearchForm(request.POST)

        if form.is_valid():
            search = Search.create_search_object_from_request(
                cleaned_data=form.cleaned_data,
                user=request.user
            )

            api_response = search_from_kiwi_api(search)
            if api_response is None:
                context['error'] = 'No results found between destinations'

            elif len(api_response['data']) == 0:
                context['error'] = 'No results found, please ' \
                                   'check dates and destinations'

            else:
                # TODO OPTIONAL optimize result creation
                results = [
                    Result.create_result_object_from_kiwi_response(
                        api_response=result,
                        search_id=search.id
                    )
                    for result in api_response['data']
                ]
                context = {
                    'itineraries': results,
                    'search': search,
                    'user': request.user,
                }

                template = 'list_results.html'
        else:
            context['form'] = form

    return render(request=request, template_name=template, context=context)


class ListSearch(LoginRequiredMixin, ListView):
    template_name = 'list_search.html'
    model = Search
    context_object_name = 'searches'

    def get_queryset(self):
        searches = Search.objects.filter(user=self.request.user)
        return searches


class DeleteAllSearch(LoginRequiredMixin, DeleteView):
    model = Search
    success_url = reverse_lazy('index')
    context_object_name = 'searches'

    def get_queryset(self):
        searches = Search.objects.filter(user=self.request.user)
        return searches

    def get_object(self, queryset=None):
        return self.get_queryset()

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            Search.delete_search(self.request.user, 0)
            messages.error(
                self.request,
                'Searches with subscriptions not deleted'
            )
            return HttpResponseRedirect(reverse_lazy('list_search'))
        return HttpResponseRedirect(success_url)



