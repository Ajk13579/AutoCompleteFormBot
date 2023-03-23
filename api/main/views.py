import datetime
import json
from json import JSONDecodeError

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import CompletedTaskPicture


def get_screenshot(request, user_id):
    """Returns a screenshot or error"""

    # Screenshot from database
    screenshot = CompletedTaskPicture.objects.filter(user_id=user_id)

    if not screenshot:
        return JsonResponse({'error': 'there is not photo yet'})

    # Making url for a screenshot
    domain = settings.SITE_URL

    if settings.SITE_URL[-1] != '/':
        domain += '/'

    full_path = domain + screenshot[0].path_for_picture

    return JsonResponse({'screenshot': full_path})


class HomeView(View):
    def post(self, request):
        # Making a normal json from b'{}'
        try:
            dictionary = json.loads(request.body.decode("utf-8"))
        except JSONDecodeError:
            dictionary = request.POST

        # Getting all parameters
        username = dictionary.get("username")
        lastname = dictionary.get("lastname")
        email = dictionary.get("email")
        phone = dictionary.get("phone")
        birthday = dictionary.get("birthday")
        user_id = dictionary.get("user_id")

        if not all([username, lastname, email, phone, birthday, user_id]):
            return JsonResponse({'error': 'invalid data'})

        # List for args in PeriodicTask
        list_of_args = [username, lastname, email, phone, birthday, user_id]

        # String formatting for better readability
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Every, for example, 30 seconds to do Periodic Task
        interval = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS)

        # Create a new task
        new_celery_task = PeriodicTask.objects.create(
            name=f'Task from {user_id}. Created at {now}',
            task='main.tasks.fill_in_form_task',
            interval=interval[0],
            args=json.dumps(list_of_args),
            start_time=datetime.datetime.now(),
            enabled=True,
        )

        # task = fill_in_form_task.delay(username, lastname, email, phone, birthday, user_id)
        return JsonResponse({'message': 'Periodic task created successfully'})

    @classmethod
    def as_view(cls, **init_kwargs):
        """For error 403"""
        view = super().as_view(**init_kwargs)
        view.csrf_exempt = True
        return view
