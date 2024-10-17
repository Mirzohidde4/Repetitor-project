from django.shortcuts import render
from rest_framework import generics
from main.models import People
from .serializers import PeopleSerializer

# Create your views here.
class PeopleApi(generics.ListAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
