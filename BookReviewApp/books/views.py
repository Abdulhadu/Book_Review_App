from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, BookSerializer, ReviewSerializer, CommentSerializer
from django.core.exceptions import PermissionDenied


@api_view()
def home(request):
    return Response({"message": "Hello, world!"})

# ------------------- User API View -----------------------
class Users(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
   
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            token, created = Token.objects.get_or_create(user=user)
            response_data = serializer.data
            response_data['token'] = token.key  
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ------------------- Book API View -----------------------
class Books(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
 
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(published_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        book = self.get_object(id)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        book = self.get_object(id)
        print(request.user)
        print(book.published_by)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if book.published_by != request.user:
        
            raise PermissionDenied("You do not have permission to edit this book.")
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        book = self.get_object(id)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if book.published_by != request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------- Review API View -----------------------
class ReviewView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id=None):
        if book_id:
            reviews = Review.objects.filter(book_id=book_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, book_id=None):
        if book_id:
            book = Book.objects.get(id=book_id)
            
            if book.published_by == request.user:
                return Response({"error": "You cannot review your own book."}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_review = Review.objects.filter(user=request.user, book=book).first()
            if existing_review:
                return Response({"error": "You have already reviewed this book."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, book=book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        if review.user != request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        if review.user != request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- Comment API View --------------------------

class CommentView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, review_id=None):

        if review_id:
            comments = Comment.objects.filter(review_id=review_id)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, review_id=None):
        if review_id:
            try:
                review = Review.objects.get(id=review_id)
            except Review.DoesNotExist:
                return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
    
            book = review.book
            print("Book is:", book)
 
            if book.published_by == request.user:
                return Response({"error": "You cannot review your own book."}, status=status.HTTP_400_BAD_REQUEST)
    
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, review=review)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    def put(self, request, comment_id=None):
        comment = Comment.objects.get(id=comment_id)
        # print("comment by" , comment.user)
        # print("User is" , request.user )
        if comment.user != request.user:
            raise PermissionDenied("You can only edit your own comments.")
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id=None):
        comment = Comment.objects.get(id=comment_id)
        # print("comment by" , comment.user)
        # print("User is" , request.user )
        if comment.user != request.user:
            raise PermissionDenied("You can only delete your own comments.")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)