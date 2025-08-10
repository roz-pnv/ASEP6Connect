from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms.user_dashboard import UserUpdateForm
from users.forms.user_dashboard import StudentUpdateForm
from users.models import Student


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_profile'] = None
        if self.request.user.is_student:
            context['student_profile'] = Student.objects.filter(user=self.request.user).first()
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
