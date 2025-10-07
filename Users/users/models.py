from django.contrib.auth.models import AbstractUser
from django.db import models

from AppCore.basics.models.models import BasicModel
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin

from .helpers import UserHelpers


class User(AbstractUser, BasicModel, ModelHelperMixin):
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        'Data de Nascimento',
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Biografia',
        blank=True,
        null=True
    )
    avatar = models.CharField(
        'Avatar',
        max_length=255,
        blank=True,
        null=True
    )
    email_verified = models.BooleanField(
        'Email Verificado',
        default=False
    )
    
    helper_class = UserHelpers
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
