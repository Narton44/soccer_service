from django.urls import path

from .views import (
    FieldsListView,
    FieldsCreateView,
    FieldsManagerListView,
    FieldsUpdateView,
    FieldsDeleteView,
    FieldsCategoryListView,
    FieldsSignCategoryListView,
    BookingsListView,
    UserBookingListView,
    UserBookingConfirmManagerView,
    SearchView
)

urlpatterns = [
    path('', 
         FieldsListView.as_view(), 
         name="home"
        ),

    path('search/', 
         SearchView.as_view(), 
         name="search"
        ),
    path('cover/<str:slug>/', 
         FieldsCategoryListView.as_view(), 
         name="category"
        ),

    path('sign/<str:slug>/', 
         FieldsSignCategoryListView.as_view(), 
         name="signcategory"
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
    path(
        'bookings/<int:pk>/',
        BookingsListView.as_view(),
        name="bookings"
    ),
    path(
        'bookings/',
        UserBookingListView.as_view(),
        name="userbookings"
    ),
    path(
        'bookings/confirm',
        UserBookingConfirmManagerView.as_view(),
        name="userbookingsconfirm"
    ),
]