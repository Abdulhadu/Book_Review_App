from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user 

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    published_by = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'published_by', 'published_date']
        read_only_fields = ['published_by', 'published_date']
        
        

# class ReviewSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

#     class Meta:
#         model = Review
#         fields = ['user', 'book', 'content']
#         read_only_fields = ['user', 'book',  'created_at', 'updated_at']
        
        
# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     review = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'review', 'content', 'created_at']
#         read_only_fields = ['user', 'review', 'created_at']


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    book = serializers.ReadOnlyField(source='book.id')

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'book', 'created_at', 'updated_at']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    review = serializers.ReadOnlyField(source='review.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'review', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'review', 'created_at', 'updated_at']