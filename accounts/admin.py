from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone', 'is_staff', 'is_blocked')
    list_filter = ('is_staff', 'is_superuser', 'is_blocked')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('phone', 'is_blocked')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
