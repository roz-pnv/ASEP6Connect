from django.contrib import admin

from .models.user import User
from .models.user import Country
from .models.student import Student
from .models.membership import Membership


admin.site.register(User)
admin.site.register(Country)
admin.site.register(Student)
admin.site.register(Membership)
