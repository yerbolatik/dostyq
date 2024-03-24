from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('sign-up/', views.RegisterView, name='sign-up'),
    path('sign-in/', views.LoginView, name='sign-in'),
    path('logout/', views.LogoutView, name='logout'),

    path('my-profile/', views.my_profile, name='my-profile'),
    path('profile/<username>', views.friend_profile, name='profile'),

    path("profile-update/", views.profile_update, name="profile-update"),

]
