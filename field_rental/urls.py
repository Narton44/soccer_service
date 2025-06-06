from django.urls import path

from .views import (
    FieldsListView,
    FieldsCreateView,
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
        )
    
]