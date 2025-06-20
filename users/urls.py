from django.urls import path

from .views import (
    RegisterUser,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserResetPasswordView,
    )

app_name = 'users'

urlpatterns = [
    path('register/',
         RegisterUser.as_view(),
         name="register"
         ),
    path('',
         UserListView.as_view(),
         name="userlist"
         ),
    path('create/',
         UserCreateView.as_view(),
         name="usercreate"
         ),
    path('update/<int:pk>/',
         UserUpdateView.as_view(),
         name="userupdate"
         ),
    path('delete<int:pk>/',
         UserDeleteView.as_view(),
         name="userdelete"
         ),
     path('user/reset-password/<int:pk>/',
          UserResetPasswordView.as_view(),
          name="useresetpassword"
          )
]