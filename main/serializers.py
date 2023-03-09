from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import *
from collections import OrderedDict

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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"

    

class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = Rate
        fields= ["comment", "user", "rate"]
    def get_user(self,obj):
        return obj.user.username 
    def get_comment(self,obj):
        if obj.comment != None:
            return obj.comment
        else:
            return None
    def to_representation(self, instance):
        result = super(CommentSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
    

class ItemSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    avg_of_rating = serializers.FloatField()
    is_recommended = serializers.BooleanField()
    comments = CommentSerializer(many=True)
    comments_count= serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ["id","title", "description", "images", "is_recommended", "location","TicketPriceForEgyptions", "TicketPriceForForeing", "TicketPriceForStudents", "videolink","nomber_of_ratings" , "workinghours_from", "workinghours_to","avg_of_rating", "views", "loves", "comments", "comments_count"]
    def get_comments_count(self, obj):
        return len(obj.comments.all())
    def to_representation(self, instance):
        result = super(ItemSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])





class ViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ["id", "user","item","views"]

class RateSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    class Meta:
        model = Rate
        fields = ["id", "user","item" , 'rate', "comment"]




class FavSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = FavList
        fields = ['item']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    trip = TripSerializer(many=True)
    class Meta:
        model = Package
        fields = ['title','duration','hotel_name','hote_location',"trip"]