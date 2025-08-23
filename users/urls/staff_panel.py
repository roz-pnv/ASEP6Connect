from django.urls import path

from users.views.staff_panel import BoardPanelView
from users.views.staff_panel import UserListView
from users.views.staff_panel import UserCreateView
from users.views.staff_panel import UserUpdateView
from users.views.staff_panel import UserDeleteView
from users.views.staff_panel import UserDetailView
from users.views.staff_panel import MembershipCreateView
from users.views.staff_panel import MembershipUpdateView
from users.views.staff_panel import MembershipDeleteView
from users.views.staff_panel import StudentCreateView
from users.views.staff_panel import StudentUpdateView
from users.views.staff_panel import StudentDeleteView

from meetings.views.meeting import StaffMeetingListView
from meetings.views.meeting import MeetingCreateView
from meetings.views.meeting import StaffMeetingDetailView
from meetings.views.meeting import MeetingUpdateView
from meetings.views.meeting import MeetingDeleteView
from meetings.views.invite import InviteCreateView
from meetings.views.invite import InviteUpdateView
from meetings.views.invite import InviteDeleteView
from meetings.views.agenda import AgendaItemCreateView 
from meetings.views.agenda import AgendaItemUpdateView
from meetings.views.agenda import AgendaItemDeleteView
from meetings.views.minutes import MinutesCreateView 
from meetings.views.minutes import MinutesUpdateView
from meetings.views.minutes import MinutesDeleteView
from meetings.views.motion import MotionDetailView

urlpatterns = [
	path("", BoardPanelView.as_view(), name="staff_panel"),
	
	path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_detail"),
    path("users/add/", UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
	
	path('membership/create/<int:user_id>/', MembershipCreateView.as_view(), name='membership_create'),
    path('membership/edit/<int:membership_id>/', MembershipUpdateView.as_view(), name='membership_edit'),
	path('membership/delete/<int:membership_id>/', MembershipDeleteView.as_view(), name='membership_delete'),
	
	path("student/create/<int:user_id>/", StudentCreateView.as_view(), name="student_create"),
    path("student/edit/<int:student_id>/", StudentUpdateView.as_view(), name="student_edit"),
    path("student/delete/<int:student_id>/", StudentDeleteView.as_view(), name="student_delete"),
	
    path('meeting/', StaffMeetingListView.as_view(), name='staff_meeting_list'),
	path('meeting/create/', MeetingCreateView.as_view(), name='meeting_create'),
	path('meeting/<int:pk>/detail/', StaffMeetingDetailView.as_view(), name='staff_meeting_detail'),
	path("meeting/edit/<int:pk>/", MeetingUpdateView.as_view(), name="meeting_edit"),
    path("meeting/delete/<int:pk>/", MeetingDeleteView.as_view(), name="meeting_delete"),
	
    path("invite/create/<int:meeting_pk>/", InviteCreateView.as_view(), name="invite_create"),
    path("invite/edit/<int:pk>/", InviteUpdateView.as_view(), name="invite_edit"),
    path("invite/delete/<int:pk>/", InviteDeleteView.as_view(), name="invite_delete"),
	
    path('agenda/create/<int:meeting_pk>/', AgendaItemCreateView.as_view(), name='agenda_create'),
    path('agenda/edit/<int:pk>/', AgendaItemUpdateView.as_view(), name='agenda_edit'),
    path('agenda/delete/<int:pk>/', AgendaItemDeleteView.as_view(), name='agenda_delete'),
	
    path("minutes/create/<int:meeting_pk>/", MinutesCreateView.as_view(), name="minutes_create"),
    path("minutes/edit/<int:pk>/", MinutesUpdateView.as_view(), name="minutes_edit"),
    path("minutes/delete/<int:pk>/", MinutesDeleteView.as_view(), name="minutes_delete"),
	
    path('motion/<int:pk>/', MotionDetailView.as_view(), name='motion_detail'),
]
