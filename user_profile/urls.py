from django.urls import path

from digital_library.views import home
from user_profile.views import AddCreditsView, Login, Logout, Profile, SignUpView

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("profile/", Profile, name="profile"),
    path("add-credits/", AddCreditsView.as_view(), name="add-credits"),
]
