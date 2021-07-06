from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('date_joined', 'last_login',)

    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_customer', 'is_agent', 'is_approved')
    list_filter = ('is_admin', 'is_customer', 'is_agent', 'is_approved')
    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('Primary Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin', 'is_customer', 'is_agent', 'is_approved')}),
        ('Time', {'fields': ('date_joined', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_admin',
                       'is_customer', 'is_agent')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.site_header = 'Loan Management System'
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
