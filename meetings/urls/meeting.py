from django.urls import path

from meetings.views.meeting import MeetingListView
from meetings.views.meeting import MeetingCreateView
from meetings.views.meeting_room import MeetingRoomView

urlpatterns = [
	path('', MeetingListView.as_view(), name='meeting_list'),
	path('create/', MeetingCreateView.as_view(), name='meeting_create'),
	path('meetings/<int:pk>/room/', MeetingRoomView.as_view(), name='meeting_room'),
]
