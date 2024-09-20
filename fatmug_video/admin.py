from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Video, Subtitle

admin.site.register(User, UserAdmin)
admin.site.register(Video)
admin.site.register(Subtitle)
