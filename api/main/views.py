import datetime
import json

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django_celery_results.models import TaskResult

from .models import CompletedTaskPicture


def get_screenshot(request, task_id):
    """Returns a screenshot or error"""

    # Take a task result of all tasks
    task = TaskResult.objects.filter(task_id=task_id)

    # Base cases
    if not task:
        return JsonResponse({'error': 'there is not task'})

    if not task[0].status == "SUCCESS":
        return JsonResponse({'error': 'task is not done yet'})

    # Screenshot from database
    screenshot = CompletedTaskPicture.objects.get(task_id=task_id)

    # Making url for a screenshot
    domain = settings.SITE_URL

    if settings.SITE_URL[-1] != '/':
        domain += '/'

    full_path = domain + screenshot.path_for_picture

    return JsonResponse({'screenshot': full_path})


class HomeView(View):
    def post(self, request):
        # Making a normal json from b'{}'
        dictionary = json.loads(request.body.decode("utf-8"))

        # Getting all parameters
        username = dictionary.get("username")
        lastname = dictionary.get("lastname")
        email = dictionary.get("email")
        phone = dictionary.get("phone")
        birthday = dictionary.get("birthday")
        user_id = dictionary.get("user_id")

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
