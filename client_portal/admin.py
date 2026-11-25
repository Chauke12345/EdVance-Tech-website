from django.contrib import admin
from .models import ProjectRequest


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):

    list_display = (
        'reference_number',
        'project_title',
        'client',
        'service',
        'budget',
        'status',
        'created_at',
    )

    list_filter = (
        'service',
        'status',
        'budget',
        'created_at',
    )

    search_fields = (
        'project_title',
        'client__username',
        'client__email',
        'business_name',
        'description',
    )

    list_editable = ('status',)

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

    fieldsets = (
        ('Client Information', {
            'fields': ('client',)
        }),
        ('Project Requirements', {
            'fields': (
                'service',
                'business_name',
                'project_title',
                'description',
                'budget',
                'preferred_completion_date',
                'supporting_document',
            )
        }),
        ('Project Management', {
            'fields': ('status', 'created_at')
        }),
    )


from .quotation_models import Quotation


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):

    list_display = (
        'reference_number',
        'project',
        'total_amount',
        'deposit_amount',
        'balance_amount',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = (
        'project__project_title',
        'project__client__username',
        'project__client__email',
    )

    readonly_fields = (
        'reference_number',
        'deposit_amount',
        'balance_amount',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Project', {
            'fields': ('project',)
        }),
        ('Quotation Details', {
            'fields': (
                'reference_number',
                'total_amount',
                'deposit_percentage',
                'deposit_amount',
                'balance_amount',
                'scope_of_work',
                'terms_and_conditions',
                'valid_until',
            )
        }),
        ('Quotation Management', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    ordering = ('-created_at',)


from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("subject", "client", "project", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = (
        "subject",
        "client__username",
        "client__email",
        "project__project_title",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = (
        "body",
        "sender__username",
        "conversation__subject",
    )
    readonly_fields = ("created_at", "read_at")
    ordering = ("-created_at",)
