from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)

from .models import Fields
from .forms import FieldForm
from .mixins import AccessMixin


class FieldsListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"

class FieldsDetailView(DetailView):
    ...


class FieldsCreateView(AccessMixin, CreateView):
    allowed_roles = ["manager",]

    model = Fields
    template_name = "addfield.html"
    form_class = FieldForm
    success_url = "/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super().form_valid(form)

class FieldsManagerListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"

    def get_queryset(self):
        return Fields.objects.filter(owner = self.request.user)

class FieldsUpdateView(UpdateView):
    ...


class FieldsDeleteView(DeleteView):
    ...







# def get_field_view(request):
#     field = Fields.objects.all()
#     context = {
#         "fields": field
#     }
#     return render(
#         request=request, 
#         template_name="index.html", 
#         context=context
#         )
