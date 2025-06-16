from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class AccessMixin(LoginRequiredMixin):
    """
    Миксин для ограничения доступа на основе собственных ролей пользователя.
    Если рольне разрешена, выполняется переадресация на указанную страницу.
    """

    allowed_roles:list = []
    redirect_url:str = '/'

    def handle_no_permission(self):
        """
        Это метод, вызывающийся если доступ запрещен.
        """
        return redirect(self.redirect_url)
    
    def dispatch(self, request, *args, **kwargs):
        """
        Этот метод проверяет соответствует ли пользователь разрешенным ролям
        перед выполнением представления.
        """

        if not request.user.is_authenticated:
            return super().handle_no_permission()
        
        user_role = getattr(request.user, 'role', None)

        if user_role not in self.allowed_roles:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

