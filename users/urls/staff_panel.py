from django.urls import path

from users.views.staff_panel import BoardPanelView
from users.views.staff_panel import UserListView
from users.views.staff_panel import UserCreateView
from users.views.staff_panel import UserUpdateView
from users.views.staff_panel import UserDeleteView

urlpatterns = [
	path("", BoardPanelView.as_view(), name="staff_panel"),
	path("users/", UserListView.as_view(), name="user_list"),
    path("users/add/", UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]
