from rest_framework import serializers


class CreateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class CreateAccountConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)

    def validate_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )

        return value
    
    
class PasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "A senha precisa ter 8 caracteres ou mais."
            )
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:    
            raise serializers.ValidationError("As senhas não conferem.")

        return data
