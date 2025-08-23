from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from meetings.models import Invite
from meetings.models import Meeting
from meetings.forms.invite import InviteForm 
from meetings.models.invite import InviteStatus
from users.views.staff_panel import BoardRoleContextMixin

class InviteCreateView(BoardRoleContextMixin, CreateView):
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


class InviteUpdateView(BoardRoleContextMixin, UpdateView):
    model = Invite
    form_class = InviteForm
    template_name = 'staff_panel/staff_meeting_management/invite_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.object.meeting  
        return context

    def get_success_url(self):
        meeting = getattr(self.object, 'meeting', None)
        if meeting:
            return reverse('staff_meeting_detail', kwargs={'pk': meeting.pk})
        return reverse('staff_meeting_list') 


class InviteDeleteView(BoardRoleContextMixin, DeleteView):
    model = Invite
    template_name = 'staff_panel/staff_meeting_management/invite_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.object.meeting  
        return context
    
    def get_success_url(self):
    	return reverse('staf_meeting_detail', kwargs={'pk': self.object.meeting.pk})


class UserInviteListView(BoardRoleContextMixin, View):
    model = Invite
    template_name = 'user/invite_list.html'
    context_object_name = 'invites'

    def get(self, request, *args, **kwargs):
        invites = Invite.objects.filter(invited_user=request.user).select_related('meeting')
        return render(request, self.template_name, {'invites': invites})
    
    def post(self, request, *args, **kwargs):
        invite_id = request.POST.get('invite_id')
        response = request.POST.get('response')

        invite = get_object_or_404(Invite, pk=invite_id, invited_user=request.user)

        if response in [InviteStatus.ACCEPTED, InviteStatus.DECLINED]:
            invite.status = response
            invite.responded_at = timezone.now()
            invite.save()

        return redirect(request.path)


class InvitationDetailView(DetailView):
    model = Invite
    template_name = 'user/invite_detail.html'
    context_object_name = 'invite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meeting = self.object.meeting
        context['meeting'] = meeting
        context['agenda_items'] = meeting.agenda_items.all()
        return context


    