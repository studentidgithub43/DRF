import uuid
from django.db import models
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.contrib.auth.models import User
from .validators import validate_file_extension
from django.db.models import UUIDField, EmailField, DateTimeField, FileField, IntegerField, CharField
    


class Account(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account_type = CharField(default="free", max_length=20)
    user = ForeignKey(User, on_delete=CASCADE, related_name="account_user", null=True, default=None, blank=True)
    total_login = IntegerField(default=0)
    company = CharField(default='', max_length=255)
    total_visit = IntegerField(default=0)
    total_document = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.account_type)

class Guest(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = EmailField(max_length = 254, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.email
    
    
class Document(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    document = FileField(blank=True, default='', validators=[validate_file_extension])
    username = ForeignKey(User, on_delete=CASCADE, related_name="doc_user", default=None, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.uuid)
    
class GuestVisit(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = ForeignKey(Guest, on_delete=CASCADE, related_name='guest_view', default=None, blank=True, null=True)
    doc_id = ForeignKey(Document, on_delete=CASCADE, related_name='document_view', default=None, blank=True, null=True)
    viewed_time = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.uuid)
    
class DocumentPageVisit(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = ForeignKey(Guest, on_delete=CASCADE, related_name='guest_page_view', default=None, blank=True, null=True)
    doc_id = ForeignKey(Document, on_delete=CASCADE, related_name='document_page_view', default=None, blank=True, null=True)
    page_num = IntegerField(default=0)
    time_spent = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.uuid)
