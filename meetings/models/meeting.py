from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()


class MeetingType(models.TextChoices):
    BOARD = 'Board_Meeting', 'Board Meeting'
    GENERAL = 'General_Assembly', 'General Assembly'
    EXTRAORDINARY = 'Extraordinary_Assembly', 'Extraordinary Assembly'


class MeetingStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SCHEDULED = 'scheduled', 'Scheduled'
    HELD = 'held', 'Held'
    CANCELED = 'canceled', 'Canceled'


class Meeting(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Descriptive title of the meeting (e.g., 'Annual Board Review')"
    )
    meeting_type = models.CharField(
        max_length=30,
        choices=MeetingType.choices,
        help_text="Type of meeting: Board, General Assembly, or Extraordinary Assembly"
    )
    status = models.CharField(
        max_length=20,
        choices=MeetingStatus.choices,
        default=MeetingStatus.SCHEDULED,
        help_text="Current status of the meeting (Draft, Scheduled, Held, or Canceled)"
    )
    created_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='created_meetings',
        help_text="User who created or organized the meeting"
    )
    date = models.DateTimeField(
        help_text="Scheduled date and time of the meeting"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Physical meeting location"
    )
    online_link = models.URLField(
        blank=True,
        null=True,
        help_text="Link for online/virtual meeting (Zoom, Teams, etc.)"
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the meeting was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last update")

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['meeting_type']),
            models.Index(fields=['date']),
            models.Index(fields=['status'])
        ]

    def __str__(self):
        return f"{self.title} ({self.get_meeting_type_display()})"
