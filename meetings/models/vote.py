from django.db import models
from django.contrib.auth import get_user_model

from meetings.models.motion import Motion

Users = get_user_model()


class VoteChoice(models.TextChoices):
    YES = 'yes', 'Yes'
    NO = 'no', 'No'
    ABSTAIN = 'abstain', 'Abstain'


class Vote(models.Model):
    motion = models.ForeignKey(
        Motion,
        on_delete=models.CASCADE,
        related_name='votes',
        help_text="Motion that this vote applies to"
    )
    voter = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='votes',
        help_text="User casting the vote"
    )
    choice = models.CharField(
        max_length=10,
        choices=VoteChoice.choices,
        help_text="Voting choice: Yes, No, Abstain"
    )
    voted_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="When the vote was cast"
    )

    class Meta:
        unique_together = ('motion', 'voter')
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f"{self.voter.username} voted {self.get_choice_display()} on {self.motion}"
