from django.views.generic import CreateView, ListView
from django.shortcuts import redirect

from users.models import CustomUser
from users.forms import CustomUserForm

class RegisterUser(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = "create_user"
    success_url = "/"
    template_name = "user/register.html"

class UserListView(ListView):
    model = CustomUser
    context_object_name = "users"
    template_name = "user/userslist.html"

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
