from django.db import models
from BookReview.models import Review 
from Auth.models import Auth

class Comment(models.Model):
    user = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on review of {self.review.book.title}"
