from django.shortcuts import render
from field_rental.models import Fields
from django.views.generic import DetailView, DeleteView, CreateView, ListView, UpdateView


class FieldsListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"


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
