from django.urls import path
from .views import login_user

urlpatterns = [
    path("api/login/", login_user, name="login_user"),
]
