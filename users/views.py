from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password

from users.models import CustomUser
from users.forms import (
    CustomUserForm, 
    CustomUserCreateForm, 
    PasswordResetForm
)

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
    
    def get_queryset(self, **kwargs):
        queryset = CustomUser.objects.all()
        return queryset

class UserCreateView(AccessMixin, CreateView):
    
    allowed_roles = ["admin", ]

    model = CustomUser
    template_name = "user/useradd.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("users:userlist")

    def form_valid(self, form):
        # создаем объект obj с помошью метода save, но не сохраняем его в базу данных
        obj = form.save(commit=False) 
        # назначаем владельцем объекта пользователя, отправившего запрос, т.е. текущего пользователя
        obj.owner = self.request.user
        # обязательно вызываем оператор return с вызовом этого же метода из базового класса
        return super().form_valid(form)

class UserUpdateView(AccessMixin, UpdateView):

    allowed_roles = ["manager", "admin"]

    model = CustomUser
    form_class = CustomUserCreateForm
    context_object_name = "userupdate"
    template_name = "user/userupdate.html"
    success_url = reverse_lazy("users:userlist")

class UserDeleteView(AccessMixin, DeleteView):

    allowed_roles = ["manager", "admin"]

    context_object_name = "userdelete"
    model = CustomUser
    template_name = "user/userdelete.html"
    success_url = reverse_lazy("users:userlist")


class UserResetPasswordView(AccessMixin, UpdateView):
    template_name = 'user/userupdate.html'
    allowed_roles = ["admin",]
    model = CustomUser
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:userlist")

    def form_valid(self, form):
        user = self.get_object()
        new_password = form.cleaned_data['new_password']
        user.password = make_password(new_password)
        user.save()
        
        return super().form_valid(form)
