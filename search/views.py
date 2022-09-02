import environ

from .api_search_easypnr import get_airport_data_from_easypnr_api
from .api_search_kiwi import search_from_kiwi_api
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from .models import Search, Result

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )

# TODO  delete search data after session

def search_view(request):
    # Check if airport data is in the database. If not, make api call and add to database
    get_airport_data_from_easypnr_api()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            search = Search.create_search_object_from_request(form.cleaned_data, request.user)

            api_response = search_from_kiwi_api(search)

            if api_response is None:

                return render(request, 'search/index.html', {'form': form,
                                                             'error': 'No results found, please check info entered'})

            results = [Result.create_result_object_from_kiwi_response(result, search.id) for result in
                       api_response['data']]

            return render(request, template_name='search/results.html', context={'itineraries': results})

        else:
            return render(request, 'search/index.html', {'form': form})
    else:
        form = SearchForm(None)
        return render(request, 'search/index.html', {'form': form})
