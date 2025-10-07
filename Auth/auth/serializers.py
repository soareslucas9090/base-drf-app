from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    type = serializers.ChoiceField(
        choices=['user', 'manager'],
        required=False,
        allow_blank=True,
        default='user'
    )
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):
        login_type = attrs.pop('type', 'user')
        
        data = super().validate(attrs)
        
        user = self.user
        
        if user.status != 1:
            raise serializers.ValidationError({
                'detail': 'Usuário inativo ou suspenso.'
            })
        
        profile = user.profiles.filter(type=login_type).first()
        
        if not profile:
            raise serializers.ValidationError({
                'detail': f'Você não possui um perfil de {login_type} cadastrado.'
            })
        
        if profile.status != 1:
            raise serializers.ValidationError({
                'detail': 'Perfil inativo ou suspenso.'
            })
        
        data['profile'] = {
            'id': profile.id,
            'type': profile.type,
            'type_display': profile.get_type_display()
        }
        
        return data
