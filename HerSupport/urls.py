from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import Health, HomePage, Login, Logout, SignUp, api_call, bot, overall

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("register", SignUp.as_view(), name="register"),
    path("login", Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("health", Health.as_view(), name="health"),
    path("api", api_call, name="api"),
    path("bot", bot, name="bot"),
    path("biomarkers", overall, name="biomarkers"),
]
