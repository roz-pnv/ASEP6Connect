from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse

from meetings.models import Invite
from meetings.models import Meeting
from meetings.forms.invite import InviteForm 

class InviteCreateView(CreateView):
    model = Invite
    form_class = InviteForm
    template_name = 'staff_panel/staff_meeting_management/invite_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.meeting = None
        if 'meeting_pk' in kwargs:
            self.meeting = get_object_or_404(Meeting, pk=kwargs['meeting_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.meeting:
            initial['meeting'] = self.meeting
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.meeting
        return context

    def get_success_url(self):
    	return reverse('staf_meeting_detail', kwargs={'pk': self.meeting.pk})


class InviteUpdateView(UpdateView):
    model = Invite
    form_class = InviteForm
    template_name = 'staff_panel/staff_meeting_management/invite_form.html'

    def get_success_url(self):
    	return reverse('staf_meeting_detail', kwargs={'pk': self.object.meeting.pk})


class InviteDeleteView(DeleteView):
    model = Invite
    template_name = 'staff_panel/staff_meeting_management/invite_confirm_delete.html'

    def get_success_url(self):
    	return reverse('staf_meeting_detail', kwargs={'pk': self.object.meeting.pk})

