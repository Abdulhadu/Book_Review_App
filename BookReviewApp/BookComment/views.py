from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import Comment, Review
from .serializer import CommentSerializer
from Auth.utils import JWTAuthentication

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes =  [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review_id = self.request.query_params.get('review_id', None)
        if review_id:
            return Comment.objects.filter(review_id=review_id)
        return Comment.objects.all().order_by('id')

    def perform_create(self, serializer):
        review_id = self.request.data.get('review')
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise PermissionDenied("Review not found.")

        book = review.book
        if book.published_by == self.request.user:
            raise PermissionDenied("You cannot comment on your own book.")

        serializer.save(user=self.request.user, review=review)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            raise PermissionDenied("You can only edit your own comments.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            raise PermissionDenied("You can only delete your own comments.")
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        return obj
