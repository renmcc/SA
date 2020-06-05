from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models

# Create your views here.


class uploadBookViewSet(ModelViewSet):
    queryset = models.uploadBook.objects.all()
    serializer_class = serializers.uploadBookSerializer
