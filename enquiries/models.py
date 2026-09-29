from django.db import models

# Create your models here.
from django.db import models


class Enquiry(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "New"
        READ = "read", "Read"
        RESOLVED = "resolved", "Resolved"

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    subject = models.CharField(max_length=150)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"