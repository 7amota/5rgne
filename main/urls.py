from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('slider' , views.SliderBaseView)
router.register('image' , views.UserImage)
urlpatterns = [
path('',include(router.urls)),
path('register/', views.SignUpView.as_view()),
path('login/', views.LoginView.as_view()),
path('update/', views.UpdateUser.as_view()),
path('profile/', views.Profile.as_view()),
path('logout/', views.Logout.as_view()),

]
