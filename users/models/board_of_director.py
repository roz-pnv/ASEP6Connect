from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()

class RoleType(models.TextChoices):
    PRESIDENT = 'President', 'President'
    VICE_PRESIDENT = 'Vice_President', 'Vice President'
    SECRETARY = 'Secretary', 'Secretary'
    TREASURER = 'Treasurer', 'Treasurer'
    TECHNICAL_OFFICER = 'technical_officer', 'Technical Officer'
    ADMISSIONS_OFFICER = 'admissions_officer', 'Admissions Officer'


class BoardOfDirector(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='board_roles',
        help_text="User serving on the board"
    )
    role_type = models.CharField(
        max_length=50,
        choices=RoleType.choices,
        help_text="Role held by the user on the board"
    )
    start_date = models.DateTimeField(
        help_text="Start date of the board role"
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="End date of the board role (if applicable)"
    )
    is_suspended = models.BooleanField(
        default=False,
        help_text="Is the board member currently suspended?"
    )

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Board Member'
        verbose_name_plural = 'Board Members'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['role_type']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
            models.Index(fields=['is_suspended']),
        ]
        unique_together = ('user', 'role_type', 'start_date')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_type_display()}"

    @property
    def is_active(self):
        """Check if the board role is currently active."""
        from datetime import datetime
        now = datetime.now()
        return (
            not self.is_suspended and
            self.start_date <= now and
            (self.end_date is None or self.end_date >= now)
        )
