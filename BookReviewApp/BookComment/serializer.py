from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    review = serializers.ReadOnlyField(source='review.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'review', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'review', 'created_at', 'updated_at']