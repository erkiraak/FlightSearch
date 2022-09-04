from .api_search_easypnr import get_airport_data_from_easypnr_api
from .api_search_kiwi import search_from_kiwi_api
from django.shortcuts import render
from django.views.generic import DetailView
from .forms import SearchForm
from .models import Search, Result


# TODO  delete search data after session

def search_view(request):
    # Check if airport data is in the database.
    # If not, make api call and add to database
    get_airport_data_from_easypnr_api()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():

            search = Search.create_search_object_from_request(
                cleaned_data=form.cleaned_data,
                user=request.user
            )

            api_response = search_from_kiwi_api(search)

            # if API call returns an error
            if api_response is None:
                context = {
                    'form': form,
                    'error': 'No results found, invalid destinations'
                }
                template = 'search/index.html'

            # if api call returns a response but no results
            elif len(api_response['data']) == 0:
                context = {
                    'form': form,
                    'error': 'No flights found, please check info entered'
                }
                template = 'search/index.html'

            # if api call returns results
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

    else:
        form = SearchForm(None)
        template = 'search/index.html'
        context = {
            'form': form,
        }

    return render(request=request, template_name=template, context=context)
