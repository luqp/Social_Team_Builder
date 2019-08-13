from django.urls import path, re_path

from . import views


app_name = "accounts"

urlpatterns = [
    path('sign_up/', views.SignUp.as_view(), name="sign_up"),
    path('sign_in/', views.SignIn.as_view(), name="sign_in"),
    path('sign_out/', views.SignOut.as_view(), name="sign_out"),
    re_path(
        r'(?P<pk>\d+)/profile/edit',
        views.EditProfileView.as_view(), name="edit"),
    re_path(
        r'(?P<pk>\d+)/profile/',
        views.ProfileView.as_view(), name="profile"),
]
