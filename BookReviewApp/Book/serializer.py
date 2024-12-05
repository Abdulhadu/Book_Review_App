from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from Auth.serializer import AuthLoginSerializer


class BookSerializer(serializers.ModelSerializer):
    published_by = AuthLoginSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'published_by', 'published_date']
        read_only_fields = ['published_by', 'published_date']
        