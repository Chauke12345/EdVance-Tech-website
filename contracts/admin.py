from django.contrib import admin
from .models import ContractTemplate, Contract, DigitalSignature


@admin.register(ContractTemplate)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "content")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "title",
        "client",
        "project",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "reference_number",
        "title",
        "client__username",
        "client__email",
        "project__project_title",
    )
    readonly_fields = (
        "reference_number",
        "template_version",
        "issued_at",
        "viewed_at",
        "signed_at",
        "created_at",
        "updated_at",
    )


@admin.register(DigitalSignature)
class DigitalSignatureAdmin(admin.ModelAdmin):
    list_display = (
        "contract",
        "signer_full_name",
        "signed_at",
        "contract_version",
    )
    search_fields = (
        "contract__reference_number",
        "signer_full_name",
        "signer__username",
    )
    readonly_fields = (
        "contract",
        "signer",
        "signer_full_name",
        "acceptance_statement",
        "typed_signature",
        "signed_at",
        "ip_address",
        "user_agent",
        "contract_version",
        "contract_snapshot",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
