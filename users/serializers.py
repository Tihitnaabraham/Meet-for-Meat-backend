from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name','phone_number', 'email', 'user_type', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user = authenticate(username=phone_number, password=password)
        if not user or not user.is_active:
            raise serializers.ValidationError('Invalid credentials or inactive user')
        attrs['user'] = user
        return attrs
