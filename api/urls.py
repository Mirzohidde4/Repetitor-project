from django.urls import path
from .views import PeopleApi

urlpatterns = [
    path('', PeopleApi.as_view()),
]