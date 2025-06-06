from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)

from .models import Fields
from .forms import FieldForm


class FieldsListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"


class FieldsCreateView(CreateView):
    model = Fields
    template_name = "addfield.html"
    form_class = FieldForm
    success_url = "/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super().form_valid(form)


class FieldsUpdateView(UpdateView):
    ...


class FieldsDeleteView(DeleteView):
    ...


class FieldsDetailView(DetailView):
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
