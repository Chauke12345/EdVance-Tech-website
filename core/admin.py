from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at', 'is_reviewed')
    list_filter = ('service', 'is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_reviewed',)
    ordering = ('-created_at',)
