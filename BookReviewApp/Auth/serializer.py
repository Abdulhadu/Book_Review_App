from BookReviewApp.base import EricModelSerializer
from .models import Auth
from rest_framework import serializers
        
class AuthSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ["Email", "Username", "Password"]
    def validate(self, attrs):
        print("Validating user data")
        if attrs['Email'] is None:
            raise serializers.ValidationError({'Email':'This field is required'})
        if attrs['Username'] is None:
            raise serializers.ValidationError({'Username':'This field is required'})
        if attrs['Password'] is None:
            raise serializers.ValidationError({'Password':'This field is required'})
        return attrs
    
class SignupSerializer(serializers.Serializer):
    Email = serializers.EmailField(max_length=50)
    Username = serializers.CharField(max_length=50)
    Password = serializers.CharField(max_length=50)
    
    def validate(self, data):
        if 'Email' not in data:
            raise serializers.ValidationError({"Email":"This field is required."})
        if 'Username' not in data:
            raise serializers.ValidationError({"Username":"This field is required."})
        if 'Password' not in data:
            raise serializers.ValidationError({"Password":"This field is required."})
        if len(data['Password']) <8 :
            raise serializers.ValidationError('Password must be 8 characters long')
        return data
    
class AuthLoginSerializer(serializers.Serializer):
    Email  = serializers.EmailField(max_length=50)
    Password = serializers.CharField(max_length=50,default=None)
        
    def validate(self, data):
        if 'Email' not in data:
            raise serializers.ValidationError({"Email":"This field is required."})
        if 'Password' not in data:
            raise serializers.ValidationError({"Password":"This field is required."})
        return data
        
    