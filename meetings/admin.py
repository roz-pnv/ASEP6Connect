from django.contrib import admin

from .models.meeting import Meeting
from .models.agenda import AgendaItem
from .models.invite import Invite
from .models.minutes import Minutes
from .models.motion import Motion
from .models.vote import Vote


admin.site.register(Meeting)
admin.site.register(AgendaItem)
admin.site.register(Invite)
admin.site.register(Minutes)
admin.site.register(Motion)
admin.site.register(Vote)
