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
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer

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

    def email(request):
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['muhammadhananasghar593@gmail.com',]
        send_mail( subject, message, email_from, recipient_list )
        return
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.email()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
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
    
class GuestAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass