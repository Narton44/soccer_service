from django.urls import path

from users.views import RegisterUser, UserListView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register"),
    path('list/', UserListView.as_view(), name="userlist"),

]