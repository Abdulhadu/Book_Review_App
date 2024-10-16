from .views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home),
    
    # Books
    path('users/', Users.as_view()),
    path('users/<int:id>/', UserDetailView.as_view()),
    path('login/', LoginView.as_view(), name='user-login'),
    
    # Books
    path('books/', Books.as_view()),
    path('books/<int:id>/', BookDetailView.as_view()), 
 
    # Reviews
    path('books/<int:book_id>/reviews/', ReviewView.as_view()),  # get post
    path('reviews/<int:review_id>/', ReviewView.as_view()),  # put delete
        
    # Comments
    path('books/<int:review_id>/comments/', CommentView.as_view()), # get post
    path('comments/<int:comment_id>/', CommentView.as_view()),  # put delete
    
]