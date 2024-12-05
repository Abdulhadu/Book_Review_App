# Review Serializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    book = serializers.ReadOnlyField(source='book.id')

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'book', 'created_at', 'updated_at']
