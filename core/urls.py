from django.contrib import admin
from django.urls import path
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
]
