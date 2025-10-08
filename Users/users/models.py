from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin

from .helpers import UserHelpers
from . import choices


class User(AbstractBaseUser, PermissionsMixin, BasicModel, ModelHelperMixin):
    name = models.CharField(
        'Nome',
        max_length=150,
    )
    email = models.EmailField('Email', unique=True)
    email_verified = models.BooleanField(
        'Email Verificado',
        default=False
    )
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
    status = models.IntegerField(
        'Status',
        choices=choices.USER_STATUS_CHOICES,
        default=choices.USER_STATUS_ATIVO
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True
    )
    is_staff = models.BooleanField(
        'Equipe',
        default=False
    )
    is_superuser = models.BooleanField(
        'Superusuário',
        default=False
    )
    date_joined = models.DateTimeField(
        'Data de Criação',
        default=timezone.now
    )

    USERNAME_FIELD = "email"
    helper_class = UserHelpers
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.name
    

class PasswordResetCode(BasicModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_code',
        verbose_name='Usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=False)
    code = models.IntegerField(null=False)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user}, code {self.code}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "code"], name="unique_code_user_constraint"
            )
        ]


class Profile(BasicModel, ModelHelperMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Usuário'
    )
    type = models.CharField(
        'Tipo',
        max_length=10,
        choices=choices.PROFILE_TYPE_CHOICES,
        default=choices.PROFILE_TYPE_USER
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
        choices=choices.PROFILE_STATUS_CHOICES,
        default=choices.PROFILE_STATUS_ATIVO
    )
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']
        unique_together = ['user', 'type']
    
    def __str__(self):
        return f'{self.user.name} - {self.get_type_display()}'
