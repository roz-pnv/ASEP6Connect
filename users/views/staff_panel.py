from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView 
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

from users.models.user import Country
from users.models.membership import MemberType
from users.models.board_of_director import BoardOfDirector, RoleType
from users.models.board_of_director import BoardOfDirector, RoleType

User = get_user_model()

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        active_role = (
            BoardOfDirector.objects.filter(user=user)
            .order_by('-start_date')
            .first()
        )
        if active_role and active_role.is_active:
            return active_role.role_type in [
                RoleType.SECRETARY,
                RoleType.PRESIDENT,
                RoleType.VICE_PRESIDENT,
                RoleType.TREASURER,
                RoleType.TECHNICAL_OFFICER,
            ]
        return False


class BoardRoleContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        active_role = (
            BoardOfDirector.objects.filter(user=user)
            .order_by('-start_date')
            .first()
        )

        context["is_secretary"] = active_role and active_role.role_type == RoleType.SECRETARY
        context["is_treasurer"] = active_role and active_role.role_type == RoleType.TREASURER
        context["is_president"] = active_role and active_role.role_type == RoleType.PRESIDENT
        context["is_vice_president"] = active_role and active_role.role_type == RoleType.VICE_PRESIDENT
        context["board_role"] = active_role

        return context

    
class BoardPanelView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, TemplateView):
    template_name = "staff_panel/panel.html"

    
class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, CreateView):
    model = User
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "gender",
        "job",
        "phone",
        "country_of_origin",
        "address",
        "language",
        "birthdate",
        "is_student",
        "is_boardofdirector",
        "is_active",
    ]
    template_name = "staff_panel/staff_user_management/user_form.html"
    success_url = reverse_lazy("user_list")


class UserListView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, ListView):
    model = User
    template_name = "staff_panel/staff_user_management/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        role = self.request.GET.get("role")
        country = self.request.GET.get("country")
        last_seen = self.request.GET.get("last_seen")

        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q))

        if role:
            qs = qs.filter(board_roles__role_type__iexact=role)

        if country:
            qs = qs.filter(country_of_origin__name__iexact=country)

        if last_seen:
            try:
                days = int(last_seen)
                threshold = timezone.now() - timedelta(days=days)
                qs = qs.filter(last_login__lt=threshold)
            except ValueError:
                pass

        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["countries"] = Country.objects.all().order_by("name")
        context["role_types"] = RoleType.choices
        context["member_types"] = MemberType.choices
        return context


class UserDetailView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, DetailView):
    model = User
    template_name = "staff_panel/staff_user_management/user_detail.html"
    context_object_name = "user"
    pk_url_kwarg = "user_id"


class UserUpdateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, UpdateView):
    model = User
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "gender",
        "job",
        "phone",
        "country_of_origin",
        "address",
        "language",
        "birthdate",
        "is_student",
        "is_boardofdirector",
        "is_active",
    ]
    template_name = "staff_panel/staff_user_management/user_form.html"
    success_url = reverse_lazy("user_list")


class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, DeleteView):
    model = User
    template_name = "staff_panel/staff_user_management/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")
