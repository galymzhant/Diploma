from django.db import models

# Create your models here.


class Application(models.Model):
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
