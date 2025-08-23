from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse

from users.views.staff_panel import BoardRoleContextMixin
from meetings.models.motion import Motion
from meetings.models.vote import VoteChoice

class MotionDetailView(BoardRoleContextMixin, DetailView):
    model = Motion
    template_name = 'staff_panel/staff_meeting_management/motion_detail.html'
    context_object_name = 'motion'

    def dispatch(self, request, *args, **kwargs):
        self.motion = get_object_or_404(Motion, pk=kwargs['pk'])
        self.meeting = self.motion.agenda_item.meeting
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        votes = self.motion.votes.select_related('voter').all()
        context.update({
            'meeting': self.meeting,
            'votes': votes,
            'vote_yes': votes.filter(choice=VoteChoice.YES).count(),
            'vote_no': votes.filter(choice=VoteChoice.NO).count(),
            'vote_abstain': votes.filter(choice=VoteChoice.ABSTAIN).count(),
            'motion_title': f'Motion on "{self.motion.agenda_item.title}" - #{self.motion.id}',
        })

        return context

    def get_success_url(self):
        return reverse('staff_meeting_detail', kwargs={'pk': self.meeting.pk})
