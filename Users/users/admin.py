"""
Admin para o app Users
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'email_verified',
        'date_joined'
    )
    
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verified',
        'date_joined'
    )
    
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'phone',
                'birth_date',
                'bio',
                'avatar',
                'email_verified'
            )
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'email',
                'phone',
                'birth_date',
                'email_verified'
            )
        }),
    )
