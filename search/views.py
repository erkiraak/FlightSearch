from .api_search_kiwi import search_from_kiwi_api
from django.db.models import ObjectDoesNotExist, Q
from django.http import JsonResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import Search, Result, Airport


def get_airport(search):
    try:
        iata = search[-4:-1]
        city = search[:-5]

        airport = Airport.objects.get(Q(iata_code=iata), Q(city=city))
    except (ObjectDoesNotExist, IndexError):
        airport = None

    return airport


def search_view(request):
    form = SearchForm(None)
    template = 'search/index.html'
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

        if request.POST['fly_from'] \
                and not isinstance(request.POST['fly_from'], Airport):
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
                context['error'] = 'No results found, invalid destinations'

            elif len(api_response['data']) == 0:
                context['error'] = 'No results found, invalid destinations'

            else:
                results = [
                    Result.create_result_object_from_kiwi_response(
                        api_response=result,
                        search_id=search.id
                    )
                    for result in api_response['data']
                ]

                context = {
                    'itineraries': results,
                    'search': search
                }

                template = 'search/list_results.html'

    return render(request=request, template_name=template, context=context)
