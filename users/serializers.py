from rest_framework import serializers

from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password', 'password1')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password1 = validated_data['password1']
        email = validated_data['email']
        if password != password1:
            raise serializers.ValidationError({"error": "Введённые пароли неверны"})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'