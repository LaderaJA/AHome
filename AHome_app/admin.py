from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Design, Like, Comment, Follow, CapturedImage



admin.site.register(Design)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(CapturedImage)



