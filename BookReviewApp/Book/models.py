from django.db import models
from Auth.models import Auth


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    published_by = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='published_books')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

