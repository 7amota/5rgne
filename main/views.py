from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status , mixins  , viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .serializers import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from .models import *
# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            # token = Token.objects.get(serializer.instance)
            response = {
            "status":1,
            "message": "User Created Successfully",
             "data": serializer.data ,
            #  "token":token.key
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

            tokens = Token.objects.get(user=user)

            response = {
                "status":1,
                "message": "Login Successfull",
                "token": tokens.key
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


class SliderBaseView(viewsets.ModelViewSet):
    queryset = Slider.objects.order_by('?')[:5]
    serializer_class = SliderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


