from django.views.generic import (
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)
from django.urls import reverse_lazy

from field_rental.models import Fields
from field_rental.forms import FieldForm
from field_rental.mixins import AccessMixin


# Field views

class FieldsListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"


class FieldsCreateView(AccessMixin, CreateView):
    allowed_roles = ["manager", "admin"]

    model = Fields
    template_name = "field_rental/addfield.html"
    form_class = FieldForm
    success_url = reverse_lazy("manager")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super().form_valid(form)

class FieldsManagerListView(AccessMixin, ListView):
    allowed_roles = ["manager", "admin"]

    model = Fields
    context_object_name = "fields"
    template_name = "field_rental/manager.html"
    
    def get_queryset(self):
        if self.request.user.role == "admin":
            return Fields.objects.all()
        else:
            return Fields.objects.filter(owner = self.request.user)

class FieldsUpdateView(AccessMixin, UpdateView):

    allowed_roles = ["manager", "admin"]

    model = Fields
    form_class = FieldForm
    context_object_name = "fields"
    template_name = "field_rental/updatefield.html"
    success_url = reverse_lazy("manager")

class FieldsDeleteView(AccessMixin, DeleteView):
    allowed_roles = ["manager", "admin"]

    context_object_name = "fields"
    model = Fields
    template_name = "field_rental/deletefield.html"
    success_url = reverse_lazy("manager")