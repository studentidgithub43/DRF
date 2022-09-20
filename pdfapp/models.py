import uuid
from django.db import models
from django.db.models import ForeignKey
from django.db.models import CASCADE
from django.contrib.auth.models import User
from django.db.models import UUIDField, EmailField, DateTimeField, FileField, CharField

class Guest(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = EmailField(max_length = 254, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.email
    
    
class Document(models.Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    document = FileField(blank=True, default='')
    username = ForeignKey(User, on_delete=CASCADE, related_name="doc_user", default=None, blank=True, null=True)
    email = ForeignKey(Guest, on_delete=CASCADE, related_name="guest_user", default=None, blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.uuid)
    