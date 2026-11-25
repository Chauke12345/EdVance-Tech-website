from django.db import models
from django.contrib.auth.models import User


class ProjectRequest(models.Model):

    SERVICE_CHOICES = [
        ('Business website', 'Business website'),
        ('Web application', 'Web application'),
        ('Business system', 'Business system'),
        ('E-commerce', 'E-commerce website'),
        ('Product development', 'Custom application / product development'),
        ('Other', 'Other'),
    ]

    BUDGET_CHOICES = [
        ('Under R2,000', 'Under R2,000'),
        ('R2,000 - R5,000', 'R2,000 - R5,000'),
        ('R5,001 - R10,000', 'R5,001 - R10,000'),
        ('R10,001 - R20,000', 'R10,001 - R20,000'),
        ('R20,001 - R50,000', 'R20,001 - R50,000'),
        ('Above R50,000', 'Above R50,000'),
        ('Not sure yet', 'Not sure yet'),
    ]

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under review', 'Under review'),
        ('Quotation sent', 'Quotation sent'),
        ('Approved', 'Approved'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
        ('Declined', 'Declined'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_requests'
    )
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    business_name = models.CharField(max_length=200, blank=True)
    project_title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    preferred_completion_date = models.DateField(null=True, blank=True)
    supporting_document = models.FileField(
        upload_to='project_requirements/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Submitted'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def reference_number(self):
        return f"EVT-{self.created_at.year}-{self.pk:05d}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Request'
        verbose_name_plural = 'Project Requests'

    def __str__(self):
        return f'{self.project_title} - {self.client.username}'


from .quotation_models import Quotation


class Conversation(models.Model):
    project = models.ForeignKey(
        ProjectRequest,
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_conversations"
    )
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        return f"{self.subject} - {self.client.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_portal_messages"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username}"
