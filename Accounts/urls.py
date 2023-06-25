from django.contrib import admin
from django.urls import path,include
from Accounts import views

urlpatterns = [
    
    path("registration",views.UserRegistrationView.as_view(),name="reg"),
    path("login",views.UserLogin.as_view(),name="login"),
    path("profile",views.Profile,name="profile"),
    path("logout",views.UserLogout.as_view(),name="logout"),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    
]