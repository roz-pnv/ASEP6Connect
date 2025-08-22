import os
import uuid

from django.db import models

from meetings.models.meeting import Meeting


def agenda_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join("meetings", "agenda_items", f"meeting_{instance.meeting.pk}", f"{uuid.uuid4()}.{ext}")


class AgendaItem(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='agenda_items',
        help_text="Meeting this agenda item belongs to"
    )
    title = models.CharField(
        max_length=255, 
        help_text="Title of the agenda item"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Detailed description of the agenda item"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order of the item within the meeting agenda"
    )
    file = models.FileField(
        upload_to=agenda_upload_path, 
        blank=True, 
        null=True, 
        help_text="Optional supporting file"
    )
    requires_vote = models.BooleanField(
        default=False, 
        help_text="Does this agenda item require voting?"
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Agenda Item'
        verbose_name_plural = 'Agenda Items'

    def __str__(self):
        return f"{self.meeting.title} - {self.title}"
