from django.shortcuts import render
from users.models import CustomUser
from django.views.generic import DetailView, DeleteView, CreateView, ListView, UpdateView


class UserDetailView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "index.html"


