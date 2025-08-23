import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model

from meetings.models.meeting import Meeting

Users = get_user_model()


def minutes_file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join("meetings", "minutes", f"meeting_{instance.meeting.pk}", f"{uuid.uuid4()}.{ext}")


class MinutesStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    APPROVED = 'approved', 'Approved'


class Minutes(models.Model):
    meeting = models.OneToOneField(
        Meeting,
        on_delete=models.CASCADE,
        related_name='minutes',
        help_text="Meeting instance this minutes record is associated with"
    )
    summary = models.TextField(
        help_text="Brief summary of the meeting outcomes and discussions"
    )
    body = models.TextField(
        blank=True,
        null=True,
        help_text="Full minutes text (optional if a file is uploaded)"
    )
    file = models.FileField(
        upload_to=minutes_file_upload_path,
        blank=True,
        null=True,
        help_text="Optional file upload for the minutes document (PDF, DOC, etc.)"
    )
    status = models.CharField(
        max_length=20,
        choices=MinutesStatus.choices,
        default=MinutesStatus.DRAFT,
        help_text="Approval status of the minutes (Draft or Approved)"
    )
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_minutes',
        help_text="User who recorded or authored the minutes"
    )
    approved_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_minutes',
        help_text="User who reviewed and approved the minutes"
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the minutes were approved"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the minutes were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last update")

    class Meta:
        verbose_name = 'Meeting Minutes'
        verbose_name_plural = 'Meeting Minutes'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['approved_at'])
        ]

    def __str__(self):
        return f"Minutes for {self.meeting.title} ({self.get_status_display()})"
