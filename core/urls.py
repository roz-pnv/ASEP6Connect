from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views.auth import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('register/', UserRegistrationView.as_view(), name='register'),
]
