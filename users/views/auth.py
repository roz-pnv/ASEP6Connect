from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms.auth import SimpleRegistrationForm

class UserRegistrationView(FormView):
    template_name = 'auth/register.html'
    form_class = SimpleRegistrationForm
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful! Welcome.")
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('home')
    