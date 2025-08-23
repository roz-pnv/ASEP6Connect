from django.db import models
from django.contrib.auth import get_user_model

from meetings.models.agenda import AgendaItem

Users = get_user_model()


class Motion(models.Model):
    agenda_item = models.ForeignKey(
        AgendaItem,
        on_delete=models.CASCADE,
        related_name='motions',
        help_text="Agenda item that this motion belongs to"
    )
    text = models.TextField(
        help_text="Text of the motion/proposal to be voted on"
    )
    created_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_motions',
        help_text="User who proposed this motion"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="When the motion was created"
    )

    def __str__(self):
        return f"Motion on {self.agenda_item.title} - {self.text[:50]}"
