from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny

from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.basics.mixins.mixins import AllowAnyMixin

from .serializers import (
    CreateAccountSerializer, CreateAccountConfirmCodeSerializer, PasswordConfirmCreateAccountSerializer
)
from .business import AccountBusiness


@extend_schema(tags=["Users.Create account"])
class CreateAccountPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = CreateAccountSerializer
    success_message = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        type_profile = serializer.get('type_profile')
        
        account_business = AccountBusiness()

        email_account_code = account_business.get_code(email, type_profile)

        account_business.send_verification_email(email, email_account_code)


@extend_schema(tags=["Users.Create account"])       
class CreateAccountConfirmCodePostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = CreateAccountConfirmCodeSerializer
    success_message = "Código verificado. Você pode prosseguir com a criação da conta."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        
        account_business = AccountBusiness()
        
        account_business.validate_code(email, code)

        
@extend_schema(tags=["Users.Create account"])
class ConfirmPasswordAccountPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = PasswordConfirmCreateAccountSerializer
    success_message = "Usuário criado com sucesso."
    
    def do_action_post(self, serializer, request):
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
