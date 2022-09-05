from .models import Search
import datetime


def cron_job_delete_search_objects_without_user():
    print(
        f'Running job at '
        f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
        f''
    )
    count = 0
    for search in Search.objects.filter(user=None):

        search.delete()
        count += 1

    print(f'Deleted {count} search objects')
