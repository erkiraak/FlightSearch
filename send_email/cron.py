import datetime

from search.api_search_kiwi import search_from_kiwi_api
from search.models import Result
from .send_email import send_email
from subscription.models import Subscription


def cron_job_send_email():
    print(
        f'Running job at '
        f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
    )

    for subscription in Subscription.objects.all():

        search = subscription.search

        api_response = search_from_kiwi_api(search)

        try:
            api_search_result = api_response['data'][0]
            result = Result.create_result_object_from_kiwi_response(
                api_response=api_search_result,
                search_id=search.id
            )
            send_email(subscription=subscription, result=result)

        except IndexError as e:
            print(e)

        except Exception as e:
            print(e)
            