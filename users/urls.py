from django.urls import path

from users.views import RegisterUser

app_name = 'users'

urlpatterns = [
    path('create/', RegisterUser.as_view(), name="create_user"),
    
]