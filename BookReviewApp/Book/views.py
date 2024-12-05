from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import Book
from .serializer import BookSerializer
from Auth.utils import JWTAuthentication

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    authentication_classes =  [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(published_by=self.request.user)

    def retrieve(self, request, pk=None):
        book = self.get_object()
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def update(self, request, pk=None):
        book = self.get_object()
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if book.published_by != request.user:
            raise PermissionDenied("You do not have permission to edit this book.")
        serializer = self.get_serializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = self.get_object()
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if book.published_by != request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        try:
            return Book.objects.get(pk=self.kwargs['pk'])
        except Book.DoesNotExist:
            return None
