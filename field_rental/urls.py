from django.urls import path

from .views import (
    FieldsListView,
    FieldsCreateView,
    FieldsManagerListView,
    FieldsUpdateView,
    FieldsDeleteView,
)

urlpatterns = [
    path('', 
         FieldsListView.as_view(), 
         name="home"
         ),
    path(
        'manager/fields/add/', 
        FieldsCreateView.as_view(), 
        name="addfields"
        ),
    path(
        'manager/fields/', 
        FieldsManagerListView.as_view(), 
        name="manager"
        ),
    path(
        'manager/fields/update/<int:pk>/', 
        FieldsUpdateView.as_view(), 
        name="updatefields"
        ),
    path(
        'manager/fields/delete/<int:pk>/', 
        FieldsDeleteView.as_view(), 
        name="deletefields"
        ),
    
    
]