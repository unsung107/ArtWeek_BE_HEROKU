from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class Musicalserializer(serializers.ModelSerializer):

    class Meta:
        model = Musical
        fields = '__all__'

class Classicserializer(serializers.ModelSerializer):

    class Meta:
        model = Classic
        fields = '__all__'
        
class Playserializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = '__all__'
        

class Complexserializer(serializers.ModelSerializer):

    class Meta:
        model = Complex
        fields = '__all__'

class Exhibitionserializer(serializers.ModelSerializer):

    class Meta:
        model = Exhibition
        fields = '__all__'


class Concertserializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = '__all__'