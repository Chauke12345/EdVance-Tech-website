from django.db import models

class Enquiry(models.Model):
    SERVICE_CHOICES = [
        ('Business website', 'Business website'),
        ('Web application', 'Web application'),
        ('Business system', 'Business system'),
        ('E-commerce', 'E-commerce'),
        ('Product development', 'Product development'),
        ('Business partnership', 'Business partnership'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f'{self.name} - {self.service}'
