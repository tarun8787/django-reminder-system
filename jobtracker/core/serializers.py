from rest_framework import serializers
from jobtracker.core.models import User
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'date_joined'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        validated_data.update({'last_login': datetime.now()})
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required= True)
    password = serializers.CharField(required=True, write_only = True)