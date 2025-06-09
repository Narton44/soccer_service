from django.urls import path

from .views import (
    FieldsListView,
    FieldsCreateView,
    FieldsManagerListView
)

urlpatterns = [
    path('', 
         FieldsListView.as_view(), 
         name="home"
         ),
    path(
        'add/field/', 
        FieldsCreateView.as_view(), 
        name="addfields"
        ),
    path(
        'manager/field/', 
        FieldsManagerListView.as_view(), 
        name="manager"
        ),
    
]