from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)
from django.urls import reverse_lazy


from ..models import Booking, Fields
from ..forms import BookingForm
from ..mixins import AccessMixin


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
    template_name = "bookings/bookinglist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field'] = Fields.objects.get(pk = self.kwargs["pk"])
        return context

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