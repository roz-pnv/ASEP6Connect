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
]
