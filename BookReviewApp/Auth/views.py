from django.contrib.auth.hashers import check_password , make_password
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .models import Auth
from BookReviewApp.base import generate_jwt_token, EricViewSet
from .serializer import AuthSignUpSerializer, SignupSerializer, AuthLoginSerializer


class SignUpViewSet(EricViewSet):
    queryset=Auth.objects
    serializer_class=AuthSignUpSerializer
    
    def create(self, request):
        try:
            email = request.data.get('Email')
            username = request.data.get('Username')
            password = request.data.get('Password')
            
            if Auth.objects.filter(Email=email).exists():
                return Response({"details": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if Auth.objects.filter(Username=username).exists():
                return Response({"details": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            #Check the input data with signupserializer to make sure it is correct.
            serializer = SignupSerializer(data=request.data)
            print("Serializer: ", serializer)
            if serializer.is_valid():
                #confirms the availability of the required fields for signup. Also checks the types of input data.
                print("Serializer is valid, email, username and password can be used")
                hashed_password = make_password(password)
                signupData = {"Email": serializer.data['Email'], "Username": serializer.data["Username"], "Password": hashed_password}
                signupSer = AuthSignUpSerializer(data=signupData)
                print("Sign up serializer data: ", signupSer)
                if signupSer.is_valid():
                    print("signup data validated")
                    signupSerData = signupSer.save()
                    print("Data saved with id: ", signupSerData.ID)
                    print(f"New user created {signupSerData.Username}")
                    return Response({"details": "User created successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({'details':signupSer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'details':serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({"details": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    def retrieve(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def list(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destory(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LoginViewSet(EricViewSet):
    queryset=Auth.objects
    serializer_class = AuthLoginSerializer
    
    def create(self, request):
        try:
            print("requested data: ", request)
            serializer = AuthLoginSerializer(data=request.data)
            print("Serializer: ", serializer)
            if serializer.is_valid():
                print("serializer got valid")
                email = serializer.validated_data['Email']
                password = serializer.validated_data['Password']
                user = Auth.objects.filter(Email=email).first()
                print("User: ", user)
                if user:
                    db_password = user.Password
                    if check_password(password, db_password):
                        token = generate_jwt_token(useremail=user.Email)
                        print("token",token)
                        print("user logged in")
                        return Response({"details":{"AccessToken":token, "UserID": user.ID}}, status=status.HTTP_200_OK)
                    else:
                        return Response({'details':'Incorrect Password'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'details':'No User found for provided Email'},status=status.HTTP_200_OK)
            else:
                return Response({'details':serializer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'details':'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed", "status": f"{status.HTTP_405_METHOD_NOT_ALLOWED}"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed", "status": f"{status.HTTP_405_METHOD_NOT_ALLOWED}"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed", "status": f"{status.HTTP_405_METHOD_NOT_ALLOWED}"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed", "status": f"{status.HTTP_405_METHOD_NOT_ALLOWED}"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def list(self, request, *args, **kwargs):
        return Response({"details": "Method not allowed", "status": f"{status.HTTP_405_METHOD_NOT_ALLOWED}"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                