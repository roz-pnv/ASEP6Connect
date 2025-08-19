from django.urls import path

from users.views.user_dashboard import UserDashboardView
from users.views.user_dashboard import ProfileUpdateView
from users.views.user_dashboard import StudentUpdateView
from users.views.user_dashboard import MembershipRequestView

urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
	path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
	path('profile/update/student/', StudentUpdateView.as_view(), name='student_profile_update'),
	path('membership/request/', MembershipRequestView.as_view(), name='membership_request'),
]
