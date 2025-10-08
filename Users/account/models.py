from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin


class EmailAccountCode(AbstractUser, BasicModel, ModelHelperMixin):
    email = models.EmailField('Email')
    code = models.CharField('Código', max_length=6, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField('Validado', default=False)
    
    class Meta:
        db_table = 'email_account_codes'
        verbose_name = 'Código de Verificação de Email'
        verbose_name_plural = 'Códigos de Verificação de Email'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
