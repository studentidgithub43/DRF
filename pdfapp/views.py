import os
from .models import Guest
from django.conf import settings
from knox.models import AuthToken
from django.contrib.auth import login
from django.core.mail import send_mail
from knox.auth import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserSerializer, RegisterSerializer, GuestSerializer, DocumentSerializer

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def email(request, email):
        subject = 'Thank you for registering to our site'
        message = 'Click of this: {}'.format(os.path.join(settings.WEB_URL, f'/api/validate/{email}/'))
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [str(email),]
        send_mail( subject, message, email_from, recipient_list )
        return
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.email(request.data.get('email'))
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Email Validation API
class ValidateAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get("username")
        user = User.objects.filter(username = username)
        if user:
            _user = user[0]
            if _user.is_active:
                return Response({"message": "User is already verified.", "status": 200})
            _user.is_active = True
            _user.save()
            return Response({"message": "User is verified.", "status": 200})
        return Response({"message": "User not found.", "status": 404})

# Password Reset API
class PasswordResetAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        print(password)
        if password != None:
            _user = request.user
            _user.set_password(password)
            _user.save()
            return Response({"message": "Password has been changed.", "status": 200})
        return Response({"message": "Password has not been changed.", "status": 404})
    
# Guest API
class GuestAPI(generics.GenericAPIView):
    serializer_class = GuestSerializer
    
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        guest = Guest.objects.filter(email=email)
        if guest:
            return Response({"message": "Guest email already found.", "status": 404})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Guest created.", "status": 200})
    
# Document Upload API
class DocumentUploadAPI(generics.GenericAPIView):
    serializer_class = DocumentSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            _username = request.data.get("username", None)
            _email = request.data.get("email", None)
            if _username != None:
                _user = User.objects.filter(username = _username)
                if _user: 
                    _user = _user[0]
                    data_to_save = request.data
                    data_to_save['username'] = _user.id  
                    serializer = self.get_serializer(data=data_to_save)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({"message": "Document has been saved.", "mode": "USER", "status": 200})
                else:
                    return Response({"message": "Particular User not found.", "mode": "USER", "status": 404})
            elif _email != None:
                _guest = Guest.objects.filter(email = _email)
                if _guest: 
                    _guest = _guest[0]
                    data_to_save = request.data
                    data_to_save['email'] = _guest.id  
                    serializer = self.get_serializer(data=data_to_save)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({"message": "Document has been saved.", "mode": "GUEST", "status": 200})
                else:
                    return Response({"message": "Particular Guest not found.", "mode": "GUEST", "status": 404})
            else:
                return Response({"message": "Must provide email or username.", "status": 404})
        except Exception as e:
            print(str(e))
            return Response({"message": "Document has not been saved.", "status": 404})