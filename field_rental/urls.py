from django.urls import path

from .views import UserDetailView

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name="home"),
]