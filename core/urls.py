from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

from users.views.auth import UserRegistrationView
from users.views.auth import LoginView
from users.views.auth import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

	path('register/', UserRegistrationView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),

	path('user/', include('users.urls.users')),  
	path('staff/', include('users.urls.staff_panel')), 

	path('meeting/', include('meetings.urls.meeting')), 

	path('finance/', include('finance.urls.wallet')), 
	path('staff/finance/', include('finance.urls.staff_panel')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
