from datetime import date
from collections import defaultdict

from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from users.models.board_of_director import BoardOfDirector
from users.models.board_of_director import RoleType
from users.models.membership import Membership
from meetings.models.vote import VoteChoice  
from users.views.staff_panel import BoardRoleContextMixin
from meetings.models.meeting import Meeting
from meetings.models.meeting import MeetingType
from meetings.models.motion import Motion
from meetings.forms.meeting_create import MeetingForm
from meetings.forms.meeting_create import AgendaItemFormSet

User = get_user_model()
    
    
class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'meeting/list.html'
    context_object_name = 'meetings'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Ensure user is authenticated before proceeding
        if not user.is_authenticated:
            return render(request, 'errors/meeting_access_denied.html')

        # Check if user is a board member
        is_board = getattr(user, 'is_boardofdirector', False)

        # Check if user has a valid, confirmed, and active membership
        has_valid_membership = Membership.objects.filter(
            user=user,
            is_active=True,
            is_confirmed=True
        ).exclude(
            membership_expiry__lt=date.today()
        ).exists()

        # Deny access if user is not board, not superuser, and has no valid membership
        if not (is_board or has_valid_membership or user.is_superuser):
            return render(request, 'errors/meeting_access_denied.html', {
                'user_id': user.id
            })

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        # Board members and superusers can view all meetings
        if user.is_boardofdirector or user.is_superuser:
            return Meeting.objects.all().order_by('-date')

        # Regular members can view:
        # - General Assembly meetings (public)
        # - Meetings they are explicitly invited to
        return Meeting.objects.filter(
            Q(meeting_type=MeetingType.GENERAL) |
            Q(invites__invited_user=user)
        ).distinct().order_by('-date')


class StaffMeetingListView(LoginRequiredMixin, BoardRoleContextMixin, ListView):
    model = Meeting
    template_name = 'staff_panel/staff_meeting_management/meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        is_board = getattr(user, 'is_boardofdirector', False)

        if not (is_board or user.is_superuser):
            return render(request, 'errors/meeting_access_denied.html')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Meeting.objects.all().order_by('-date')


class MeetingCreateView(LoginRequiredMixin, BoardRoleContextMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'staff_panel/staff_meeting_management/meeting_form.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        active_role = (
            BoardOfDirector.objects.filter(user=user)
            .order_by('-start_date')
            .first()
        )
        if not (user.is_superuser or (active_role and active_role.role_type in [RoleType.PRESIDENT, RoleType.SECRETARY])):
            return render(request, 'errors/meeting_access_denied.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agenda_formset'] = AgendaItemFormSet(
			self.request.POST or None,
			self.request.FILES or None,
			prefix='agendaitems'
		)
        context['users'] = User.objects.filter(is_active=True).order_by('first_name')
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        agenda_formset = context['agenda_formset']

        form.instance.created_by = self.request.user
        self.object = form.save()

        if agenda_formset.is_valid():
            for agenda_form in agenda_formset:
            	if agenda_form.cleaned_data:
                    agenda_item = agenda_form.save(commit=False)
                    agenda_item.meeting = self.object
                    agenda_item.save()
            
        invited_user_ids = self.request.POST.getlist('invited_users')
        for user_id in invited_user_ids:
            try:
                user = User.objects.get(id=user_id)
                self.object.invites.create(invited_user=user)
            except User.DoesNotExist:
                continue

        return redirect('meeting_list') 


class StaffMeetingDetailView(LoginRequiredMixin, BoardRoleContextMixin, DetailView):
    model = Meeting
    template_name = 'staff_panel/staff_meeting_management/meeting_detail.html'
    context_object_name = 'meeting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meeting = self.get_object()

        context['agenda_items'] = meeting.agenda_items.all() if hasattr(meeting, 'agenda_items') else []

        context['invitees'] = meeting.invites.all() if hasattr(meeting, 'invites') else []

        context['minutes'] = getattr(meeting, 'minutes', None)

        motions = Motion.objects.filter(agenda_item__meeting=meeting).select_related('agenda_item')
        context['motions'] = motions if motions.exists() else []
        
        votes_by_motion = defaultdict(lambda: None)
        for motion in motions:
            votes_by_motion[motion.id] = motion.votes.select_related('voter').all()
            
        context['votes_by_motion'] = votes_by_motion
        
        return context


class MeetingUpdateView(BoardRoleContextMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'staff_panel/staff_meeting_management/meeting_update.html'

    def get_success_url(self):
        return reverse('staff_meeting_detail', kwargs={'pk': self.object.pk})


class MeetingDeleteView(BoardRoleContextMixin, DeleteView):
    model = Meeting
    template_name = 'staff_panel/staff_meeting_management/meeting_confirm_delete.html'

    def get_success_url(self):
        return reverse('staff_meeting_list')