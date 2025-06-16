from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DeleteView
)
from django.shortcuts import redirect

from users.models import CustomUser
from users.forms import CustomUserForm
from field_rental.mixins import AccessMixin

class RegisterUser(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = "create_user"
    success_url = "/"
    template_name = "user/register.html"

class UserListView(AccessMixin, ListView):
    model = CustomUser
    context_object_name = "users"
    template_name = "user/userslist.html"

    allowed_roles = ["admin",]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return redirect('home')
            
    def post(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            self.object = None
            return super().post(request, *args, **kwargs)
        else:
            return redirect('home')
    
    def get_queryset(self, **kwargs):
        queryset = CustomUser.objects.all()
        return queryset


class UserUpdateView(AccessMixin, UpdateView):
    ...

class UserCreateView(AccessMixin, CreateView):
    ...

class UserDeleteView(AccessMixin, DeleteView):
    ...
