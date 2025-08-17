from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms.user_dashboard import UserUpdateForm
from users.forms.user_dashboard import StudentUpdateForm
from users.forms.user_dashboard import MembershipRequestForm
from users.models import Student
from users.models import Membership


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Student Profile
        context['student_profile'] = None
        if self.request.user.is_student:
            context['student_profile'] = Student.objects.filter(user=self.request.user).first()
        
        # Latest Membership
        context['membership'] = Membership.objects.filter(user=self.request.user).order_by('-created_at').first()
        
        context['membership_history'] = Membership.objects.filter(user=self.request.user).order_by('-created_at')

        return context


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'user/profile_update.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            if user.is_student: 
                return redirect('student_profile_update')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})
    

class StudentUpdateView(LoginRequiredMixin, View):
    template_name = 'user/student_profile_update.html'

    def get(self, request):
        student_profile, created = Student.objects.get_or_create(user=request.user)
        form = StudentUpdateForm(instance=student_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        student_profile, created = Student.objects.get_or_create(user=request.user)
        form = StudentUpdateForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})
        

class MembershipRequestView(LoginRequiredMixin, CreateView):
    model = Membership
    form_class = MembershipRequestForm
    template_name = 'membership/request_membership.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        latest_membership = Membership.objects.filter(user=request.user).order_by('-created_at').first()

        if latest_membership:
            if latest_membership.is_confirmed and not latest_membership.is_expired:
                messages.warning(request, "You already have an active membership.")
                return redirect('dashboard')
            
            elif not latest_membership.is_confirmed and not latest_membership.is_expired:
                messages.warning(request, "Your membership request is already pending.")
                return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        membership = form.save(commit=False)
        membership.user = self.request.user
        membership.is_confirmed = False  
        membership.is_active = False
        membership.save()
        messages.success(self.request, "Your membership request has been submitted and is pending approval.")
        return super().form_valid(form)
