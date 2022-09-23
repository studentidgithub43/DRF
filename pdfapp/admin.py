from django.contrib import admin
from .models import Guest, Document, GuestVisit, DocumentPageVisit, Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'total_login', 'company', 'total_visit', 'total_document', 'created_at', 'uuid']

class GuestsAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'uuid']
    
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['username', 'document', 'created_at', 'uuid']
    
class GuestVisitAdmin(admin.ModelAdmin):
    list_display = ['email', 'doc_id', 'viewed_time', 'created_at', 'uuid']

class DocumentPageVisitAdmin(admin.ModelAdmin):
    list_display = ['email', 'doc_id', 'page_num', 'time_spent', 'created_at', 'uuid']

admin.site.register(Guest, GuestsAdmin)
admin.site.register(Document, DocumentsAdmin)
admin.site.register(GuestVisit, GuestVisitAdmin)
admin.site.register(DocumentPageVisit, DocumentPageVisitAdmin)
admin.site.register(Account, AccountAdmin)