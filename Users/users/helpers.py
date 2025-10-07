from AppCore.core.helpers.helpers import ModelInstanceHelpers


class UserHelpers(ModelInstanceHelpers):
    
    def add_profile(self, profile_type, bio='', avatar='', status=1):
        """
        Adiciona um novo perfil ao usuário.
        
        Args:
            profile_type: Tipo do perfil ('user' ou 'manager')
            bio: Biografia do perfil
            avatar: Avatar do perfil
            status: Status do perfil (0=Inativo, 1=Ativo, 2=Suspenso)
            
        Returns:
            Profile: O perfil criado ou None se já existir
        """
        from .models import Profile
        
        existing_profile = self.object_instance.profiles.filter(type=profile_type).first()
        if existing_profile:
            return None
        
        profile = Profile.objects.create(
            user=self.object_instance,
            type=profile_type,
            bio=bio,
            avatar=avatar,
            status=status
        )
        return profile
    
    def get_profiles(self):
        """Retorna todos os perfis do usuário"""
        return self.object_instance.profiles.all()
    
    def has_profile_type(self, profile_type):
        """Verifica se o usuário possui um perfil do tipo especificado"""
        return self.object_instance.profiles.filter(type=profile_type).exists()

