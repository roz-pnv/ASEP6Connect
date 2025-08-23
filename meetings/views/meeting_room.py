from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages

from meetings.models.meeting import Meeting
from meetings.models.motion import Motion
from meetings.models.vote import Vote
from meetings.models.vote import VoteChoice
from meetings.forms.motion import MotionCreateForm

class MeetingRoomView(LoginRequiredMixin, DetailView):
    model = Meeting
    template_name = 'meeting/room.html'
    context_object_name = 'meeting'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['motions'] = Motion.objects.filter(agenda_item__meeting=self.object)
        context['votes'] = Vote.objects.filter(motion__agenda_item__meeting=self.object)
        context['user_votes'] = {
            vote.motion_id: vote.choice
            for vote in Vote.objects.filter(
                motion__agenda_item__meeting=self.object,
                voter=self.request.user
			)
		}
        context['motion_form'] = MotionCreateForm(meeting=self.object)
        
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'create_motion' in request.POST:
            form = MotionCreateForm(request.POST, meeting=self.object)
            if form.is_valid():
                motion = form.save(commit=False)
                motion.created_by = request.user
                motion.save()
                messages.success(request, "Motion created successfully.")
            else:
                messages.error(request, "Failed to create motion.")
            return redirect(request.path)

        elif 'vote_motion' in request.POST:
            motion_id = request.POST.get('motion_id')
            choice = request.POST.get('choice')
            motion = get_object_or_404(Motion, id=motion_id, agenda_item__meeting=self.object)
            
            existing_vote = Vote.objects.filter(motion=motion, voter=request.user).first()
            if existing_vote:
                messages.warning(request, "You have already voted on this motion.")
            elif choice in VoteChoice.values:
                Vote.objects.create(
					motion=motion,
					voter=request.user,
					choice=choice
				)
                messages.success(request, "Your vote has been recorded.")
            else:
                messages.error(request, "Invalid vote choice.")
                
            return redirect(request.path)


        return redirect(request.path)
