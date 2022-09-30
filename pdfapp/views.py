import os
from django.db.models import F
from django.conf import settings
from knox.models import AuthToken
from django.http import JsonResponse
from django.contrib.auth import login
from django.core.mail import send_mail
from knox.auth import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Guest, Document, GuestVisit, DocumentPageVisit, Account
from .serializers import UserSerializer, RegisterSerializer, GuestSerializer, DocumentSerializer, GuestVisitSerializer, DocumentPageVisitSerializer
from .serializers import AccountSerializer

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        Account.objects.filter(user__username=request.data.get("username")).update(total_login=F('total_login') + 1)
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
        user = User.objects.filter(username=request.data.get("username"))
        if user:
            return Response({"message": "User already found.", "status": 400})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _user = User.objects.get(username=request.data.get('username'))
        account_serializer = AccountSerializer(data={
            "account_type": request.data.get("type"),
            "user": _user.id
        })
        account_serializer.is_valid(raise_exception=True)
        account_serializer.save()
        # self.email(request.data.get('email'))
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
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            data_to_save = request.data
            data_to_save['username'] = request.user.id  
            serializer = self.get_serializer(data=data_to_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Account.objects.filter(user__username=request.user.username).update(total_document=F('total_document') + 1)
            return Response({"message": "Document has been saved.", "status": 200})
        except Exception as e: 
            if "Unsupported file extension." in str(e):
                return Response({"message": "Accept only PDF.", "status": 404})
            return Response({"message": "Document has not been saved.", "status": 404})

# Get all Documents
class DocumentsViewAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        documents = [
            {
                "uuid": doc.uuid,
                "document": doc.document.path,
                "username": doc.username.username,
                "created_at": doc.created_at
            }
            for doc in Document.objects.all()
            ]
        return JsonResponse(documents, safe=False)

class GuestVisitsViewAPI(generics.GenericAPIView):
    serializer_class = GuestVisitSerializer
    
    def get(self, request, *args, **kwargs):
        return JsonResponse([
            {
                "uuid": gv.uuid,
                "email": gv.email.email,
                "doc_path": gv.doc_id.document.path,
                "doc_id": gv.doc_id.uuid,
                "viewed_time": gv.viewed_time,
                "created_at": gv.created_at
            }
            for gv in GuestVisit.objects.all()
            ], safe=False)
    
    def post(self, request, *args, **kwargs):
        _doc_id = request.data.get("doc_id", None)
        _email = request.data.get("email", None)
        _doc = Document.objects.filter(uuid=_doc_id)
        _guest = Guest.objects.filter(email=_email)
        if not _doc:
            return Response({"message": "Wrong Document ID", "status": 404})
        if not _guest:
            return Response({"message": "Wrong Guest Email", "status": 404})
        try:
            data_to_save = request.data
            data_to_save['email'] = _guest[0].id
            data_to_save['doc_id'] = _doc[0].id
            serializer = self.get_serializer(data=data_to_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Changes have been saved.", "status": 200})
        except Exception as e:
            return Response({"message": "Changes have not been saved.", "status": 404})
            
            
# Document Page Visit API
class DocumentPageVisitAPIView(generics.GenericAPIView):
    serializer_class = DocumentPageVisitSerializer
    def get(self, request, *args, **kwargs):
        return JsonResponse([
            {
                "uuid": dpv.uuid,
                "email": dpv.email.email,
                "doc_path": dpv.doc_id.document.path,
                "doc_id": dpv.doc_id.uuid,
                "page_num": dpv.page_num,
                "time_spent": dpv.time_spent,
                "created_at": dpv.created_at
            }
            for dpv in DocumentPageVisit.objects.all()
            ], safe=False)
    
    def post(self, request, *args, **kwargs):
        _doc_id = request.data.get("doc_id", None)
        _email = request.data.get("email", None)
        _doc = Document.objects.filter(uuid=_doc_id)
        _guest = Guest.objects.filter(email=_email)
        if not _doc:
            return Response({"message": "Wrong Document ID", "status": 404})
        if not _guest:
            return Response({"message": "Wrong Guest Email", "status": 404})
        try:
            data_to_save = request.data
            data_to_save['email'] = _guest[0].id
            data_to_save['doc_id'] = _doc[0].id
            serializer = self.get_serializer(data=data_to_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Changes have been saved.", "status": 200})
        except Exception as e:
            return Response({"message": "Changes have not been saved.", "status": 404})