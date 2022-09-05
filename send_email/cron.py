from search.api_search_kiwi import search_from_kiwi_api
from search.models import Result
from .send_email import send_email
from subscription.models import Subscription
import datetime


# class SendEmailCronJob(CronJobBase):
#     RUN_EVERY_MINUTES = 2  # every 1 minutes
#     RETRY_AFTER_FAILURE_MINUTES = 1
#     schedule = Schedule(
#         run_every_mins=RUN_EVERY_MINUTES,
#         retry_after_failure_mins=RETRY_AFTER_FAILURE_MINUTES
#     )
#     code = 'send_email.my_send_email_cron_job'  # a unique code

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
            print("sending email")
            send_email(subscription=subscription, result=result)

        except IndexError as e:
            print(e)

        except Exception as e:
            print(e)

#
# class CleanSearchCronJob(CronJobBase):
#     RUN_EVERY_MINUTES = 1  # every 1 minutes
#     RETRY_AFTER_FAILURE_MINUTES = 1
#     schedule = Schedule(
#         run_every_mins=RUN_EVERY_MINUTES,
#         retry_after_failure_mins=RETRY_AFTER_FAILURE_MINUTES
#     )
#     code = 'send_email.my_send_email_cron_job'  # a unique code
#
#     def do(self):
#         print("Cleaning data")
