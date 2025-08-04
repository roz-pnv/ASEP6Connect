from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()

class MemberType(models.TextChoices):
    MAIN = 'main', 'Main'
    ASSOCIATE = 'associate', 'Associate'
    VOLUNTEER = 'volunteer', 'Volunteer'
    HONORARY = 'honorary', 'Honorary'


class Membership(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='memberships',
        help_text="The user associated with this membership"
    )
    member_type = models.CharField(
        max_length=20,
        choices=MemberType.choices,
        help_text="Type of membership (Main, Associate, Volunteer, Honorary)"
    )
    can_vote = models.BooleanField(
        default=False,
        help_text="Is the member eligible to vote?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the membership currently active?"
    )
    is_confirmed = models.BooleanField(
        default=False,
        help_text="Has the membership been officially confirmed?"
    )
    membership_expiry = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the membership expires"
    )
    confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date and time when the membership was confirmed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when the membership record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date when the membership record was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['member_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['can_vote']),
            models.Index(fields=['membership_expiry']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_member_type_display()}"

    @property
    def is_expired(self):
        """Check if the membership has expired."""
        return self.membership_expiry and self.membership_expiry < date.today()
