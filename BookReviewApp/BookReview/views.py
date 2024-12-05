from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import Review, Book
from .serializer import ReviewSerializer
from Auth.utils import JWTAuthentication

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def get_queryset(self):
        book_id = self.request.query_params.get('book_id', None)
        print("book_id is : ", book_id)
        if book_id:
            return Review.objects.filter(book_id=book_id)
        return Review.objects.all().order_by('id')

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        book = Book.objects.get(id=book_id)
        print("book_id is : ", book_id)
        if book.published_by == self.request.user:
            raise PermissionDenied("You cannot review your own book.")

        existing_review = Review.objects.filter(user=self.request.user, book=book).first()
        if existing_review:
            raise PermissionDenied("You have already reviewed this book.")

        serializer.save(user=self.request.user, book=book)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        return obj
