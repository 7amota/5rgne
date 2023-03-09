from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
import requests

def log(message):
    bot_token = "5960259924:AAHVATbYlByUUfxXh0bNWhdViAvUSClZONI"
    groub_id = 1409161603
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={groub_id}&parse_mode=Markdown&text={message}"
    requests.get(url)




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    image = models.ImageField(upload_to='Photos/%y/%m/%d',null=True , blank=True)
    username = models.CharField(max_length=45)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Slider(models.Model):
    imageUrl = models.URLField()
            



# 1. item
# title, description, Gellary[images], location,
#  opening hours, Ticketprice for [egyptions, student, foreign], reviews, vidlink[opt]
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=500)
    TicketPriceForEgyptions = models.CharField(max_length=50)
    TicketPriceForStudents = models.CharField(max_length=50)
    TicketPriceForForeing = models.CharField(max_length=50)
    videolink = models.URLField(max_length=800, null=True, blank=True)
    workinghours_from = models.FloatField(null=True , blank=True)
    workinghours_to = models.FloatField(null=True , blank=True)
    is_recommended = models.BooleanField(default=False ,null=True , blank=True)
    avg = models.FloatField(null=True , blank=True)
    item_views = models.IntegerField(null=True , blank=True)
    likes = models.IntegerField(null=True , blank=True)
    def __str__(self):
        return self.title
    def nomber_of_ratings(self):
         ratings = Rate.objects.filter(item=self)
         return len(ratings)
    def avg_of_rating(self):
        stars = 0
        ratings = Rate.objects.filter(item=self)
        for x in ratings:
            stars += x.rate
        if len(ratings) > 0:
            return stars / len(ratings)

        else:
            return 0

    def views(self):
        view = View.objects.filter(item=self)
        no = 0
        for i in view:
            no += i.views
        if no == 0:
            return "no views"
        return no

    def loves(self):
        loves = FavList.objects.filter(item=self)
        num = 0
        for i in loves:
            num += i.love
        if num == 0:
            return 0
        return num

 



@receiver(post_save, sender=Item)
def item_save(sender,instance,created=False, **kwargs):
    if created:
        log(f"Item created: {instance}")
        

@receiver(pre_save, sender=Item)
def update(sender, **kwargs):
        item = kwargs['instance']
        log(f'Updated item {item}')

        # views
        view = View.objects.filter(item=item)
        no = 0
        for i in view:
            no += i.views
            item.item_views = no
        if no == 0:
            item.item_views = 0

        # stars
        stars = 0
        ratings = Rate.objects.filter(item=item)
        for x in ratings:
            stars += x.rate

        if len(ratings) > 0:
            item.avg = stars / len(ratings )
        else:
            item.avg = 0


        loves = FavList.objects.filter(item=item)
        num = 0
        for i in loves:
            num += i.love
            item.likes = num
        if num ==0:
            item.likes = 0
        



        

            

        # if item.avg == 5:

        #     Item.objects.filter(pk=item.id).update(is_recommended=True)

            

            
    
        




class Images(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to='Item', null=True , blank=True )


# Rating
class Rate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    item = models.ForeignKey(Item ,on_delete=models.CASCADE, related_name="comments")
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField( null=True, blank=True,max_length=150)
    

    class Meta:
        unique_together = ('user', 'item')
        index_together = ('user' , 'item')
     





class FavList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    item = models.ForeignKey(Item ,on_delete=models.CASCADE,related_name="itemser")
    love = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(1)])
    is_liked = models.BooleanField(null=True,blank=True)
    class Meta:
       constraints = [
            models.UniqueConstraint(fields=['user', 'item'], name='name of constraint')
        ]


@receiver(post_save, sender=FavList)
def Favlist_save(sender,instance,created=False, **kwargs):
    if created:
        log(f"Fav added: {instance}")


class View(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    item = models.ForeignKey(Item ,on_delete=models.CASCADE)
    views = models.IntegerField(validators=[MaxValueValidator(1)])




# 2. package
# duration of the trip, hotel[name, locat]
class Package(models.Model):
    title = models.CharField(max_length=450)
    duration = models.CharField(max_length=300)
    hotel_name = models.CharField(max_length=50)
    hote_location = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Trip(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name="trip")
    location = models.CharField(max_length=250)
    image1 = models.ImageField(upload_to="Photos/%y/%m/%d",null=True,blank=True,)
    image2 = models.ImageField(upload_to="Photos/%y/%m/%d",null=True,blank=True,)
    image3 = models.ImageField(upload_to="Photos/%y/%m/%d",null=True,blank=True,)
    image4 = models.ImageField(upload_to="Photos/%y/%m/%d",null=True,blank=True,)
    





# trip program [sitename, images]

@receiver(post_save, sender=Package)
def Favlist_save(sender,instance,created=False, **kwargs):
    if created:
        log(f"Package added: {instance}")
