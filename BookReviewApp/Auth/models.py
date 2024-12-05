from django.db import models

# Create your models here.

class Auth(models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    Email = models.CharField(max_length=255, unique=True)
    Username = models.CharField(max_length=255, unique=True)
    Password = models.CharField(max_length=255)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'Email'
    
    class Meta:
        ordering = ['ID']

    def __str__(self):
        return self.Username
    
    @property
    def is_authenticated(self):
        return True