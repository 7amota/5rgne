from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status , mixins  , viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from .serializers import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from .models import *
from django.db.models import Avg
import requests
import os , json



def log(message):
    bot_token = "5960259924:AAHVATbYlByUUfxXh0bNWhdViAvUSClZONI"
    groub_id = 1409161603
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={groub_id}&parse_mode=Markdown&text={message}"
    requests.get(url)



class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data )
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.get(user=serializer.instance)
            log(message=f"account created: data:{request.data}")
            response = {
            "status":1,
            "message": "User Created Successfully",
             "data": serializer.data ,
            "token":token.key
             }
            return Response(data=response, status=status.HTTP_201_CREATED)
        message = {
            "status":0,
            "message": "some thing went wrong ! ",
             "data": serializer.errors ,
            }
            
        return Response(message, status=status.HTTP_400_BAD_REQUEST)




class LoginView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class=AuthTokenSerializer

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens, created = Token.objects.get_or_create(user=user)
            log(message=f"user logged in email={email}, password={password}, token={tokens}")
            response = {
                "status":1,
                "message": "Login Successfull",
                "id": tokens.user_id,
                "token": tokens.key
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)




class UpdateUser(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user ,data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
                return Response({
                    "status":0,
                    "message":"some thing went wrong"
                }, status=status.HTTP_200_OK)
        
        response = {
            "status" : 1,
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

        


class SliderBaseView(viewsets.ModelViewSet):
    queryset = Slider.objects.order_by('?')[:5]
    serializer_class = SliderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        response = {
            "message" : "method POST/CREATE work in admin panel"
        }
        return Response(response , status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
            response = {
                "message" : "method PUT/UPDATE work in admin panel"
            }
            return Response(response , status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
            response = {
                "message" : "method DELETE work in admin panel"
            }
            return Response(response , status.HTTP_200_OK)
    
    



class UserImage(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user , data=request.FILES,context={"request": 
                      request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user
        ,context={"request":request} 
        )
        response = {
            "status" : 1,
            "data" : serializer.data
        }
        return Response(response, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user , data=request.FILES, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "status": 1,
            "message": "updated successfully",
            "data":serializer.data
        }
        return Response(serializer.data , status.HTTP_200_OK)




class Profile(generics.RetrieveAPIView):
    # queryset = Token.objects.all()
    
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        token = Token.objects.get(user=user)
        serializer = self.serializer_class(user
        ,context={"request": request}
        
        )
        return Response(
            {
                "status":1,
                "data":serializer.data,
                "token":token.key,
                
            }
        )




class Logout(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
         log(message=f"user loggedout: {request.user}")
         request.user.auth_token.delete()
         response = {
             "status" : 1,
             "message":"user is gone ):"
         }
         return Response(response , status.HTTP_410_GONE)




class GetItem(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    def get(self, request:Request, *args, **kwargs):
        item = Item.objects.all()
        serializer = self.serializer_class(item , many=True, context={"request": request})
        response = {
            'items' : serializer.data,

        }
        log(message=f"Request to get items from {request.user},{response}")
        return Response(response, status.HTTP_200_OK)




class Addview(generics.CreateAPIView):
    queryset = View.objects.all()
    serializer_class = ViewsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
       
            item = Item.objects.get(pk=request.data["itemid"]) 
            viewsl = request.data['view']
            user = request.user
            
            view = View.objects.create(user=user , item=item , views=viewsl)
            data = ViewsSerializer(view, many=False)
            
            item.save()
            json = {
                    'status': 1,
                    'message':"created successfully",
                    'data':data.data

                }
            log(message=json)
            return Response(json , status.HTTP_200_OK)




class Addrate(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
           item = Item.objects.get(id=request.data["itemid"])
           stars = request.data['stars']
           user = request.user
           
           try:
                print(request.user)

                rate = Rate.objects.get(user=user.id , item=item.id)
                rate.rate = stars
                if "comment" in request.data:
                    rate.comment = request.data["comment"]
                rate.save()
                item.save()
                serializerupdate = RateSerializer(rate , many=False)
                json = {
                    'message' : 'updated',
                    'data': serializerupdate.data
                }
                log(message=json)
                return Response(json, status.HTTP_200_OK)

            
           except:
                print(request.user)
                def get_comment():
                    if "comment" in request.data:
                        return request.data["comment"]
                    else:
                        return None

                createrate = Rate.objects.create(
                    item=item , user=user , rate=stars , comment=get_comment()
                )
                serializer = RateSerializer(createrate, many=False)
                item.save()
                jsonr = {
                    'message' : 'created',
                    'data' : serializer.data
                }
                log(message=jsonr)
                return Response(jsonr, status=status.HTTP_200_OK)
    def get(self, request, *args, **kwargs):
        rat = Rate.objects.get(user=request.user , item = request.data["itemid"])
        serializer = self.serializer_class(rat)
        

        json = {
            "status":1,
            "data":serializer.data
        }
        return Response(json, status.HTTP_200_OK)




class Fav(generics.ListCreateAPIView):
    queryset = FavList.objects.all()
    serializer_class = FavSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        item = request.data["itemid"]
        user = request.user
        getitem = Item.objects.get(id=item)

        try:
            get = self.queryset.get(item=item , user=user)
            if get:

                get.delete()
                getitem.save()
                
            
            j = {
                "status":1,
                "message":"item deleted successfully"
            }
            return Response(j, status.HTTP_200_OK)
        except:
            getitem = Item.objects.get(id=item)
            create = self.queryset.create(user=user , item=getitem, love=1)
            getitem.save()
            data = self.serializer_class(create)
            
            json = {
                "status":1,
                "message":"item added successfully",
                "data":data.data,
            }
            log(message=json)
            return Response(json,status.HTTP_200_OK)
    def get(self, request:Request, *args, **kwargs):
        user = request.user
        fav = self.queryset.filter(user=user)
        data = self.serializer_class(fav, many=True)
        return Response(data.data, status.HTTP_200_OK)

class SearchforItem(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    def get(self, request, *args, **kwargs):
         title = request.data["title"]
         item = self.queryset.filter(title__icontains=title)
         data = self.serializer_class(item)
         return Response(data.data , status.HTTP_200_OK)         

class MostRecent(generics.ListAPIView):
    queryset = Item.objects.filter().order_by("-id")
    serializer_class = ItemSerializer


class RecommendedItems(generics.ListAPIView):
    queryset = Item.objects.filter().order_by("-item_views")
    serializer_class= ItemSerializer


class FavCheck(generics.CreateAPIView):
    queryset = FavList.objects.all()
    serializer_class = FavSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        itemid= request.data["itemid"]
        item = Item.objects.get(pk=itemid)
        item.save()
        if self.queryset.filter(item=item, user=request.user):
            mes = {
                "status":1,
                "message":"check response is : True"
            }
            return Response(mes, status=status.HTTP_200_OK)
        else:
            les = {
                "status":0,
                "message":"check response is : False"
            }
            return Response(les, status=status.HTTP_200_OK)


class JSONFileView(APIView):
     def get(self,request):
         with open(os.path.join("main/city.json"), "r", encoding="UTF-8") as r:
             jsondata = json.load(r)
         return Response(jsondata)


class PackageView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class GetComments(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, itemid, *args, **kwargs):
        item = Item.objects.get(pk=itemid)
        comment = self.queryset.filter(item=item)
        data = self.serializer_class(comment ,many=True)
        return Response(data.data , status.HTTP_200_OK)
        
