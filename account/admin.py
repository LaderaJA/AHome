from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_moderator')
    list_filter = ('is_staff', 'is_active', 'is_moderator')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'date_of_birth', 'location', 'is_moderator')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'date_of_birth', 'location', 'is_moderator')}),
    )
