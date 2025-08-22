from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from meetings.models import Minutes, Meeting
from meetings.forms.minutes import MinutesForm
from users.views.staff_panel import BoardRoleContextMixin

class MinutesCreateView(BoardRoleContextMixin, CreateView):
    model = Minutes
    form_class = MinutesForm
    template_name = 'staff_panel/staff_meeting_management/minutes_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.meeting = get_object_or_404(Meeting, pk=kwargs['meeting_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['meeting'] = self.meeting
        initial['recorded_by'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.meeting
        return context

    def get_success_url(self):
        return reverse('staff_meeting_detail', kwargs={'pk': self.meeting.pk})


class MinutesUpdateView(BoardRoleContextMixin, UpdateView):
    model = Minutes
    form_class = MinutesForm
    template_name = 'staff_panel/staff_meeting_management/minutes_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.object.meeting
        return context

    def get_success_url(self):
        return reverse('staff_meeting_detail', kwargs={'pk': self.object.meeting.pk})


class MinutesDeleteView(BoardRoleContextMixin, DeleteView):
    model = Minutes
    template_name = 'staff_panel/staff_meeting_management/minutes_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting'] = self.object.meeting
        return context

    def get_success_url(self):
        return reverse('staff_meeting_detail', kwargs={'pk': self.object.meeting.pk})
