from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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

from users.models import Membership
from users.models import Student 
from users.models.user import Country
from users.models.membership import MemberType
from users.models.board_of_director import BoardOfDirector
from users.models.board_of_director import RoleType
from users.forms.staff_membership import MembershipForm
from users.forms.staff_student import StudentForm  


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
        member_type = self.request.GET.get("member_type")
        is_student = self.request.GET.get("is_student")
        joined_after = self.request.GET.get("joined_after")
        joined_before = self.request.GET.get("joined_before")

        if joined_after:
            qs = qs.filter(created_at__date__gte=joined_after)
        if joined_before:
            qs = qs.filter(created_at__date__lte=joined_before)

        if is_student == "true":
            qs = qs.filter(is_student=True)
        elif is_student == "false":
            qs = qs.filter(is_student=False)

        if member_type:
            qs = qs.filter(
                memberships__member_type=member_type,
                memberships__is_active=True,
                memberships__membership_expiry__gte=timezone.now()
            )
            
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q))

        if role:
            qs = qs.filter(board_roles__role_type__iexact=role)

        if country:
            qs = qs.filter(country_of_origin__name__iexact=country)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        current_membership = user.memberships.order_by("-created_at").first()
        context["membership"] = current_membership

        all_memberships = user.memberships.order_by("-created_at")
        context["all_memberships"] = all_memberships

        student_profile = Student.objects.filter(user=user).first()
        context["student"] = student_profile

        return context


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


class MembershipCreateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = "staff_panel/staff_user_management/membership_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=self.kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.user.id})


class MembershipUpdateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = "staff_panel/staff_user_management/membership_form.html"
    pk_url_kwarg = "membership_id"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.object.user.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object.user
        return context


class MembershipDeleteView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, DeleteView):
    model = Membership
    template_name = "staff_panel/staff_user_management/membership_confirm_delete.html"
    pk_url_kwarg = "membership_id"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.object.user.id})


class StudentDetailView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, DetailView):
    model = Student
    template_name = "staff_panel/staff_student_management/student_detail.html"
    context_object_name = "student"
    pk_url_kwarg = "student_id"


class StudentCreateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'staff_panel/staff_user_management/student_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.user  
        return context

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.object.user.id})


class StudentUpdateView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "staff_panel/staff_user_management/student_form.html"
    pk_url_kwarg = "student_id"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.object.user.id})
    

class StudentDeleteView(LoginRequiredMixin, StaffRequiredMixin, BoardRoleContextMixin, DeleteView):
    model = Student
    template_name = "staff_panel/staff_user_management/student_confirm_delete.html"
    pk_url_kwarg = "student_id"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"user_id": self.object.user.id})
