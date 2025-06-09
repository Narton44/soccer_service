from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('field_rental.urls')),
    path('user/', include('django.contrib.auth.urls')),
]
