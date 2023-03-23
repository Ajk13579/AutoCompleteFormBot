from django.urls import path

from .views import HomeView, get_screenshot

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('get-screenshot/<str:user_id>', get_screenshot, name="get_screenshot"),
]