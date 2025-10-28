import random, string

from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.common.util.util import send_simple_email
from AppCore.common.texts.emails import EMAIL_CREATE_ACCOUNT
from AppCore.common.texts.emails import EMAIL_PASSWORD_RESET

from BaseDRFApp import settings
from Users.users.models import User
from .models import EmailAccountCode
from .rules import AccountRule
from .helpers import AccountHelper


class AccountBusiness(ModelInstanceBusiness):   
    def _get_code(self):
        try:
            length_code = 6
            
            return ''.join(random.choices(string.ascii_lowercase, k=length_code))
        except Exception as e:
            raise e
        
    
    def get_code(self, email, type_profile):
        try:
            account_rules = AccountRule()

            account_rules.user_profile_dont_exists(email, type_profile)

            account_helper = AccountHelper()
            
            account_helper.del_codes_expired(email)

            random_code = self._get_code()
            
            return EmailAccountCode.objects.create(
                email=email,
                code=random_code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de verificação.')
        
    def send_verification_email(self, email, email_account_code):
        try:
            send_simple_email(
                "Recuperação de senha",
                f"Código de recuperação de senha: {email_account_code.code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                EMAIL_CREATE_ACCOUNT % email_account_code.code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')
        
    def validate_code(self, email, code):
        try:
            email_account_code = EmailAccountCode.objects.get(
                email=email, code=code
            )

            email_account_code.is_validated = True
            email_account_code.save()
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Código inválido.')
        
    def create_user_account(self, email, code, name, password, phone=None, birth_date=None, type_profile=None, bio=None):
        try:
            account_helper = AccountHelper()
            
            account_helper.validate_valid_code(email, code)
            
            User.objects.create_user(
                email=email,
                name=name,
                password=password,
                phone=phone,
                birth_date=birth_date,
                profiles=[{
                    'type': type_profile,
                    'bio': bio,
                }]
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível criar a conta do usuário.')
   # NOVOS MÉTODOS PARA RECUPERAÇÃO DE SENHA
    
    def get_password_reset_code(self, email, type_profile):
        try:
            account_rules = AccountRule()

            account_rules.user_profilet_exists(email, type_profile)

            account_helper = AccountHelper()
            
            account_helper.del_codes_expired(email)

            random_code = self._get_code()
            
            return EmailAccountCode.objects.create(
                email=email,
                code=random_code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de verificação.')
    
    def send_password_reset_email(self, email, reset_code):
        """
        Envia email com código de recuperação de senha
        """
        try:
            # Crie um template específico para reset de senha
            email_subject = "Recuperação de Senha"
            email_message = f"Seu código de recuperação de senha é: {reset_code.code}"
            
            send_simple_email(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                # EMAIL_PASSWORD_RESET % reset_code.code  # Crie este template
                EMAIL_PASSWORD_RESET % reset_code.code  # Usando o mesmo por enquanto
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de recuperação.')
    
    def validate_password_reset_code(self, email, code):
        """
        Valida o código de recuperação de senha
        """
        try:
            email_account_code = EmailAccountCode.objects.get(
                email=email, code=code
            )

            email_account_code.is_validated = True
            email_account_code.save()
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Código inválido.')
    
    def reset_user_password(self, email, code, new_password):
        """
        Redefine a senha do usuário após validação do código
        """
        try:
            # Valida o código novamente (por segurança)
            self.validate_password_reset_code(email, code)
            
            # Busca o usuário
            user = User.objects.get(email=email)
            
            # Define a nova senha
            user.set_password(new_password)
            user.save()
            
            # Invalida o código (impede reutilização)
            # Você pode deletar o código ou marcar como usado
            email_account_code = EmailAccountCode.objects.get(
                email=email, 
                code=code
            )
            email_account_code.delete()  # Ou marcar com um campo 'is_used'
            
            return True
            
        except User.DoesNotExist:
            raise SystemErrorException('Usuário não encontrado.')
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível redefinir a senha.')