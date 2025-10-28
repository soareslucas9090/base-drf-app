from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny

from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.basics.mixins.mixins import AllowAnyMixin

from .serializers import (
    CreateAccountSerializer, CreateAccountConfirmCodeSerializer, PasswordConfirmCreateAccountSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmCodeSerializer, PasswordResetNewPasswordSerializer
)
from .business import AccountBusiness

from AppCore.core.permissions.permissions import AllowAnyPermission
@extend_schema(tags=["Users.Create account"])
class CreateAccountPostView(BasicPostAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        type_profile = serializer.get('type_profile')
        
        account_business = AccountBusiness()
        email_account_code = account_business.get_code(email, type_profile)
        account_business.send_verification_email(email, email_account_code)


@extend_schema(tags=["Users.Create account"])       
class CreateAccountConfirmCodePostView(BasicPostAPIView):
    serializer_class = CreateAccountConfirmCodeSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Código verificado. Você pode prosseguir com a criação da conta."
    
    def do_action_post(self, serializer, request):
        # CORREÇÃO: Acesse diretamente como dicionário
        email = serializer.get('email')
        code = serializer.get('code')
        
        account_business = AccountBusiness()
        account_business.validate_code(email, code)

        
@extend_schema(tags=["Users.Create account"])
class ConfirmPasswordAccountPostView(BasicPostAPIView):
    serializer_class = PasswordConfirmCreateAccountSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Usuário criado com sucesso."
    
    def do_action_post(self, serializer, request):
        # CORREÇÃO: Acesse diretamente como dicionário
        email = serializer.get('email')
        code = serializer.get('code')
        password = serializer.get('password')
        phone = serializer.get('phone')
        birth_date = serializer.get('birth_date')
        type_profile = serializer.get('type_profile')
        bio = serializer.get('bio')
        name = serializer.get('name')
        
        account_business = AccountBusiness()
        account_business.create_user_account(
            email, code, name, password, phone, birth_date, type_profile, bio
        )
        
        return {
            'message': 'Usuário criado com sucesso.',
            'status_code': status.HTTP_201_CREATED
        }
    
@extend_schema(tags=["Users.Password Reset"])
class PasswordResetRequestPostView(BasicPostAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Código de recuperação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        type_profile = serializer.get('type_profile')

        account_business = AccountBusiness()
        
        # Gera código de recuperação
        reset_code = account_business.get_password_reset_code(email,type_profile)
        
        # Envia email com código
        account_business.send_password_reset_email(email, reset_code)


@extend_schema(tags=["Users.Password Reset"])
class PasswordResetConfirmCodePostView(BasicPostAPIView):
    serializer_class = PasswordResetConfirmCodeSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Código verificado. Você pode definir uma nova senha."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        
        account_business = AccountBusiness()
        
        # Valida o código de recuperação
        account_business.validate_password_reset_code(email, code)


@extend_schema(tags=["Users.Password Reset"])
class PasswordResetNewPasswordPostView(BasicPostAPIView):
    serializer_class = PasswordResetNewPasswordSerializer
    permission_classes = [AllowAnyPermission]
    success_message = "Senha redefinida com sucesso."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        new_password = serializer.get('new_password')
        
        account_business = AccountBusiness()
        
        # Redefine a senha do usuário
        account_business.reset_user_password(email, code, new_password)
        
        return {
            'message': 'Senha redefinida com sucesso.',
            'status_code': status.HTTP_200_OK
        }