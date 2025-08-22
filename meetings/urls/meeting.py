from django.urls import path

from meetings.views.meeting import MeetingListView

urlpatterns = [
	path('', MeetingListView.as_view(), name='meeting_list'),
]
