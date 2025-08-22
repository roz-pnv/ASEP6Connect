from django.urls import path

from meetings.views.meeting import MeetingListView
from meetings.views.meeting import MeetingCreateView

urlpatterns = [
	path('', MeetingListView.as_view(), name='meeting_list'),
	path('create/', MeetingCreateView.as_view(), name='meeting_create'),
]
