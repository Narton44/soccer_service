from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import CustomUser
from users.forms import (
    CustomUserForm, 
    CustomUserCreateForm, 
    PasswordResetForm,
    CustomUserSettingsForm,
    CustomUserUpdateForm
)

from field_rental.mixins import AccessMixin

class RegisterUser(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = "create_user"
    success_url = "/"
    template_name = "user/register.html"

    def form_valid(self, form):
        # Сохраняем форму, но делаем пользователя неактивным после сохранения
        response = super().form_valid(form)
        
        # Делаем пользователя неактивным
        user = self.object
        user.is_active = False
        user.save()
        
        # Отправляем email с подтверждением
        self.send_confirmation_email(user)
        
        messages.warning(
            self.request, 
            "Аккаунт создан, пожалуйста подтвердите его пройдя по ссылке, "
            "отправленной на указанный Вами Email."
        )
        
        return response

    def send_confirmation_email(self, user):
        """Отправка email с подтверждением регистрации"""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        confirmation_url = self.request.build_absolute_uri(
            reverse('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        )
        
        subject = "Подтверждение регистрации"
        message = render_to_string('user/email_confirmation.html', {
            'user': user,
            'confirmation_url': confirmation_url,
        })
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=message,
            fail_silently=False,
        )

def confirm_email(request, uidb64, token):
    """Обработка подтверждения email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Ваш email успешно подтвержден! Добро пожаловать!")
        return redirect('home')  # Убедитесь, что у вас есть URL с именем 'home'
    else:
        messages.error(request, "Ссылка подтверждения недействительна или устарела.")
        return redirect('users:register')  # Перенаправляем обратно на регистрацию



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
    form_class = CustomUserCreateForm
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
    form_class = CustomUserUpdateForm
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
    
class UserUpdateSettingsView(AccessMixin, UpdateView):
    template_name = 'user/userupdate.html'
    allowed_roles = ["admin", "manager", "user"]
    model = CustomUser
    form_class = CustomUserSettingsForm


    def get_object(self):
        obj = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        
        if self.request.user != obj:
            raise PermissionDenied("У вас нет доступа!")
        
        return obj
    
@login_required
def change_password_view(request):
    """смена пароля из пользовательских настроек"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Ваш пароль успешно обновлён")
            return redirect("home")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/changepassword.html', {"form":form})

