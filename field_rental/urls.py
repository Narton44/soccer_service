from django.urls import path

from .views import FieldsListView

urlpatterns = [
    path('', FieldsListView.as_view(), name="home"),
]