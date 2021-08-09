from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.utils.translation import gettext as _

from . models import User

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email','username','name')
    list_filter = ('email','username','name','is_active','is_staff')
    ordering = ('-joined_at',)
    list_display = ('email','id','username','name','is_active','is_staff','is_verified')
    fieldsets = (
        (None, {'fields': ('email','username')}),
        (_('Personal Info'), {'fields':('name', 'avatar', 'city', 'country')}),
        (_('Permissions'), {'fields':('is_active','is_staff','is_superuser','is_verified')}),
    )
    formfield_overrides = {
        models.TextField: {'widget':Textarea(attrs={'rows':20,'cols':60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','name','password1','password2','is_staff','is_active','is_superuser')
        }),
    )

admin.site.register(User, UserAdminConfig)
