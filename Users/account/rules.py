from AppCore.core.rules.rules import ModelInstanceRules

from .helpers import AccountHelper


class AccountRule(ModelInstanceRules):
    def user_profile_dont_exists(self, email, type_profile):
        account_helper = AccountHelper()
        
        if account_helper.user_with_email_and_type_profile_exists(email, type_profile):
            self.return_exception(
                'Já existe um usuário com este email para este perfil.'
            )
        
        return True
    def user_profilet_exists(self, email, type_profile):
        account_helper = AccountHelper()
        
        if account_helper.user_with_email_and_type_profile_exists(email, type_profile):
            return True
        
        self.return_exception(
            'Não existe um usuário com este email para este perfil.'
        )
        
