from rest_framework import serializers, authentication, exceptions
from .models import Auth
import jwt
from django.conf import settings

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = Auth.objects.filter(Email=payload['Email']).first()
            if user is None:
                raise exceptions.AuthenticationFailed('User not found.')
            return (user, None)  # Return user and None for the auth token
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')
    
def get_auth_by_token(request):
    try:
        jwt_auth = JWTAuthentication()
        auth = jwt_auth.authenticate(request=request)
        # auth = AllUsers.objects.filter(Email = auth[0])
        if auth:
            return auth[0]
        else:
            return None
    except exceptions.AuthenticationFailed:
        return exceptions.AuthenticationFailed

