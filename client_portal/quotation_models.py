from decimal import Decimal
from django.db import models
from .models import ProjectRequest


class Quotation(models.Model):

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Sent', 'Sent to client'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Expired', 'Expired'),
    ]

    project = models.ForeignKey(
        ProjectRequest,
        on_delete=models.PROTECT,
        related_name='quotations'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    deposit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('50.00')
    )

    scope_of_work = models.TextField()
    terms_and_conditions = models.TextField(blank=True)

    valid_until = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'

    @property
    def reference_number(self):
        return f'EVQ-{self.created_at.year}-{self.pk:05d}'

    @property
    def deposit_amount(self):
        if self.total_amount is None or self.deposit_percentage is None:
            return Decimal('0.00')
        return (
            self.total_amount * self.deposit_percentage
            / Decimal('100')
        ).quantize(Decimal('0.01'))

    @property
    def balance_amount(self):
        if self.total_amount is None:
            return Decimal('0.00')
        return self.total_amount - self.deposit_amount

    def __str__(self):
        return f'{self.reference_number} - {self.project.project_title}'
