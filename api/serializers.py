from rest_framework import serializers
from main.models import People


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('user_id',  'fullname', 'phone', 'second_phone', 'monthly')
