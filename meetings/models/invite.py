from django.db import models
from django.contrib.auth import get_user_model

from meetings.models.meeting import Meeting

Users = get_user_model()


class InviteStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'


class Invite(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='invites',
        help_text="Meeting this invite belongs to"
    )
    invited_user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='meeting_invites',
        help_text="User who was invited to the meeting"
    )
    status = models.CharField(
        max_length=20,
        choices=InviteStatus.choices,
        default=InviteStatus.PENDING,
        help_text="Response status of the invite"
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the invite was sent"
    )
    responded_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the invite was responded to"
    )

    class Meta:
        verbose_name = "Meeting Invite"
        verbose_name_plural = "Meeting Invites"
        unique_together = ('meeting', 'invited_user')
        indexes = [
            models.Index(fields=['meeting']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"Invite: {self.invited_user.username} -> {self.meeting.title} ({self.get_status_display()})"
