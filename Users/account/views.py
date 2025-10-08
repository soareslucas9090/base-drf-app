import random, string

from django.utils import timezone
from drf_spectacular.utils import (
    extend_schema,
)
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny

from BaseDRFApp import settings
from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.common.util.util import send_simple_email
from AppCore.common.texts.emails import EMAIL_CREATE_ACCOUNT

from Users.users.models import User
from .serializers import (
    CreateAccountSerializer, CreateAccountConfirmCodeSerializer, PasswordConfirmSerializer
)
from .models import EmailAccountCode


@extend_schema(tags=["Users.Create account"])
class CreateAccountPostView(BasicPostAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [AllowAny]
    success_message = "Código de verificação enviado para o email informado."
    
    def _exists_user(self, email):
        if User.object.filter(email=email).exists():
            return {
                'message': 'Já existe um usuário com este email.',
                'status_code': status.HTTP_404_NOT_FOUND
            }
            
    def _del_codes_expired(self, email):
        EmailAccountCode.objects.filter(
            Q(
                created_at__lt=timezone.now() - timezone.timedelta(minutes=30)
            ) | Q(
                email=email
            )
        ).delete()
        

    def _get_code(self, email):
        self._exists_user(email)
        
        self._del_codes_expired(email)
        
        length_code = 6
        
        return ''.join(random.choices(string.ascii_lowercase, k=length_code))
        
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        
        random_code = self._get_code(email)
        
        email_account_code = EmailAccountCode.objects.create(
            email=email,
            code=random_code
        )
        
        send_simple_email(
            "Recuperação de senha",
            f"Código de recuperação de senha: {email_account_code.code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            EMAIL_CREATE_ACCOUNT.format(code=email_account_code.code)
        )

        
class CreateAccountConfirmCodePostView(BasicPostAPIView):
    serializer_class = CreateAccountConfirmCodeSerializer
    permission_classes = [AllowAny]
    
    def do_action_post(self, serializer, request):
    
        email = serializer.get('email')
        code = serializer.get('code')

        email_account_code = EmailAccountCode.objects.get(
            email=email, code=code
        )

        email_account_code.is_validated = True
        email_account_code.save()


class ConfirmPasswordAccountPostView(BasicPostAPIView):
    serializer_class = PasswordConfirmSerializer
    permission_classes = [AllowAny]
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        password = serializer.get('password')

        email_account_code = EmailAccountCode.objects.get(
            email=email, code=code, is_validated=True
        )

