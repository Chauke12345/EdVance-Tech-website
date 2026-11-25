from django.conf import settings
from django.db import models
from django.utils import timezone


class ContractTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Contract(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent to client"),
        ("Viewed", "Viewed by client"),
        ("Signed", "Signed"),
        ("Declined", "Declined"),
        ("Expired", "Expired"),
        ("Cancelled", "Cancelled"),
    ]

    template = models.ForeignKey(
        ContractTemplate,
        on_delete=models.PROTECT,
        related_name="contracts"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="contracts"
    )
    project = models.ForeignKey(
        "client_portal.ProjectRequest",
        on_delete=models.PROTECT,
        related_name="contracts"
    )
    quotation = models.ForeignKey(
        "client_portal.Quotation",
        on_delete=models.PROTECT,
        related_name="contracts",
        null=True,
        blank=True
    )
    reference_number = models.CharField(max_length=40, unique=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    template_version = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )
    issued_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference_number and self.pk is None:
            super().save(*args, **kwargs)
        if not self.reference_number:
            self.reference_number = f"EVC-{timezone.now():%Y}-{self.pk:05d}"
            super().save(update_fields=["reference_number"])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number or 'New contract'} - {self.title}"


class DigitalSignature(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.PROTECT,
        related_name="digital_signature"
    )
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="contract_signatures"
    )
    signer_full_name = models.CharField(max_length=200)
    acceptance_statement = models.TextField()
    typed_signature = models.CharField(max_length=200)
    signed_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    contract_version = models.PositiveIntegerField()
    contract_snapshot = models.TextField()

    def __str__(self):
        return f"{self.signer_full_name} - {self.contract.reference_number}"
