from django.contrib import admin
from .models import Complaint, Response

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'student', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['complaint_id', 'subject', 'student__username']
    readonly_fields = ['complaint_id', 'created_at', 'updated_at']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'responder', 'responded_at']
    list_filter = ['responded_at']