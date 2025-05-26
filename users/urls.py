from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView

    )
from users.views import RegisterUser, UserListView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register"),
    path('list/', UserListView.as_view(), name="userlist"),

    #path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password_reset/done/",
    #     PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]