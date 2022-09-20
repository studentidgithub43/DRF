from django.contrib import admin
from .models import Guest, Document


class GuestsAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'email', 'created_at']
    
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'document', 'email', 'username']
    
admin.site.register(Guest, GuestsAdmin)
admin.site.register(Document, DocumentsAdmin)