from django.contrib import admin

# Register your models here.
from apps.users.models import User

admin.site.register(User)