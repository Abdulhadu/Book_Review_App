from django.db import models
from Book.models import Book
from Auth.models import Auth

class Review(models.Model):
    user = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"