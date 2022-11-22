# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from .models import Detail, Identification

User = get_user_model()
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'email', 'password')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'gender', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['first_name'],validated_data['last_name'], validated_data['email'], validated_data['password'])

        return user

# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password')


# class RegistrationSerializer(serializers.ModelSerializer): 
#     password = serializers.CharField(max_length = 15,null=True)
#     confirm_password = serializers.CharField(max_length = 15,null=True) 
#     class Meta:
#         model = User
#         fields = [
#             'first_name',
#             'last_name',
#             'gender',
#             "email",
#             "password",
#         ]
#         extra_kwargs = {"password": {"write_only": True}}
#         password = self.validated_data["password"]
#         user.set_password(password)
#         user.save()
#         return user


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields =  '__all__' 


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'         