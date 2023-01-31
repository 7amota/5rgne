from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('slider' , views.SliderBaseView)
urlpatterns = [
path('',include(router.urls)),
path('register/', views.SignUpView.as_view()),
path('login/', views.LoginView.as_view()),
]
