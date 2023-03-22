import json

from django.http import HttpResponse
from django.views import View

from .tasks import add


class HomeView(View):
    def post(self, request):
        dictionary = json.loads(request.body.decode("utf-8"))

        username = dictionary.get("username")
        lastname = dictionary.get("lastname")
        email = dictionary.get("email")
        phone = dictionary.get("phone")
        birthday = dictionary.get("birthday")

        print(add.delay(username, lastname, email, phone, birthday))

        return HttpResponse("Working")

    @classmethod
    def as_view(cls, **init_kwargs):
        view = super().as_view(**init_kwargs)
        view.csrf_exempt = True
        return view
