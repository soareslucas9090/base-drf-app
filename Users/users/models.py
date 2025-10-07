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
    email_verified = models.BooleanField(
        'Email Verificado',
        default=False
    )
    status = models.IntegerField(
        'Status',
        choices=(
            (0, 'Inativo'),
            (1, 'Ativo'),
            (2, 'Suspenso'),
        ),
        default=1
    )
    
    helper_class = UserHelpers
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username


class Profile(BasicModel, ModelHelperMixin):
    PROFILE_TYPE_CHOICES = (
        ('user', 'Usuário'),
        ('manager', 'Gestor'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Usuário'
    )
    type = models.CharField(
        'Tipo',
        max_length=10,
        choices=PROFILE_TYPE_CHOICES,
        default='user'
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
    status = models.IntegerField(
        'Status',
        choices=(
            (0, 'Inativo'),
            (1, 'Ativo'),
            (2, 'Suspenso'),
        ),
        default=1
    )
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']
        unique_together = ['user', 'type']
    
    def __str__(self):
        return f'{self.user.username} - {self.get_type_display()}'
