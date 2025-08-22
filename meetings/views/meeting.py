from datetime import date

from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from meetings.models.meeting import Meeting
from meetings.models.meeting import MeetingType
from users.models.membership import Membership  


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
