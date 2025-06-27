from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)
from django.urls import reverse_lazy

from .models import Fields
from .models import Booking
from .forms import FieldForm
from .forms import BookingForm
from .mixins import AccessMixin


# Field views

class FieldsListView(ListView):
    model = Fields
    context_object_name = "fields"
    template_name = "index.html"

class FieldsDetailView(DetailView):
    ...

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

# Booking views

class BookingsCreateView(AccessMixin, CreateView):
    allowed_roles = ["manager", "admin", "user"]

    model = Booking
    template_name = "bookingcreate.html"
    form_class = BookingForm
    success_url = reverse_lazy("bookings:bookinglist")

class BookingsListView(ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookinglist.html"

class BookingsDetailView(DetailView):
    model = Booking
    context_object_name = "bookingdetail"
    template_name = "bookingdetail.html"

class BookingsUpdateView(AccessMixin, UpdateView):

    allowed_roles = ["manager", "admin"]

    model = Booking
    form_class = BookingForm
    context_object_name = "bookingupdate"
    template_name = "bookingupdate.html"
    success_url = reverse_lazy("bookings:bookinglist")

class BookingsDeleteView(AccessMixin, DeleteView):
    allowed_roles = ["manager", "admin"]

    context_object_name = "bookingsdelete"
    model = Booking
    template_name = "bookingdelete.html"
    success_url = reverse_lazy("bookings:bookinglist")







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
