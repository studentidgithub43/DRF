from re import search
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DocumentPageVisit, Guest, Document, GuestVisit, Account


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Account Serializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_type', 'user')

# Guests Serializer
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            email = validated_data['email'], 
            password = validated_data['password'], 
            is_active = False
            )
        return user
    
# Document Serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'document', 'username')


# Document Serializer
class GuestVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestVisit
        fields = ('id', 'email', 'doc_id', 'viewed_time')
        
# Document Page Visit Serializer
class DocumentPageVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentPageVisit
        fields = ('id', 'email', 'doc_id', 'page_num', 'time_spent')