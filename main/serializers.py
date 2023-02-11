from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "id"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()


        return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    image = serializers.ImageField()
    class Meta:
        model = User
        fields = ["email", "username", "password", 'id' , "image"]

    def update(self, instance, validated_data,):
       password = self.validated_data.pop("password")
       images = validated_data.pop('image', None)
     
       if password is not None:
           instance.set_password(password)

       instance.save()
       
       return instance

        

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["imageUrl"]

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = User
        fields = ["image", "id"]
