import datetime
import json

from django.http import JsonResponse
from django.views import View
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class HomeView(View):
    def post(self, request):
        dictionary = json.loads(request.body.decode("utf-8"))

        username = dictionary.get("username")
        lastname = dictionary.get("lastname")
        email = dictionary.get("email")
        phone = dictionary.get("phone")
        birthday = dictionary.get("birthday")

        user_id = dictionary.get("user_id")

        list_of_args = [username, lastname, email, phone, birthday, user_id]

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        interval = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)

        new_celery_task = PeriodicTask.objects.create(
            name=f'Task from {user_id}. Created at {now}',
            task='main.tasks.fill_in_form_task',
            interval=interval,
            args=json.dumps(list_of_args),
            start_time=datetime.datetime.now(),
            enabled=True,
        )

        # task = fill_in_form_task.delay(username, lastname, email, phone, birthday, user_id)

        return JsonResponse({'message': 'Periodic task created successfully'})

    @classmethod
    def as_view(cls, **init_kwargs):
        view = super().as_view(**init_kwargs)
        view.csrf_exempt = True
        return view
