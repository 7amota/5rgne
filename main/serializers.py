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
    class Meta:
        model = User
        fields = ["email", "username", "password", 'id']
    


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    image = serializers.ImageField()
    class Meta:
        model = User
        fields = ["email", "username", "password", 'id' , "image"]


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["imageUrl"]

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = User
        fields = ["image", "id"]
    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     photo_url = obj.image.url
    #     return request.build_absolute_uri(photo_url)

# prt2




class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id","title", "description", "location", "TicketPriceForEgyptions", "TicketPriceForForeing", "TicketPriceForStudents", "videolink", "image1","image2" , "image3","nomber_of_ratings" ,"avg_of_rating", "views",]




class ViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ["id", "user","item","views"]

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ["id", "user","item" , 'rate']

class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavList
        fields = ['id' , 'user' , 'item']