from django.views.generic import CreateView

from users.models import CustomUser
from users.forms import CustomUserForm

class RegisterUser(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = "create_user"
    success_url = "/"
    template_name = "register.html"
