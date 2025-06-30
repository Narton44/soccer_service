from django.views.generic import (
    DetailView, 
    DeleteView, 
    CreateView, 
    ListView, 
    UpdateView
)
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.utils import timezone



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

    def get_queryset(self):
        today_start = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        today_end = today_start + timedelta(days=7)
        
        queryset =  Booking.objects.filter(field__pk = self.kwargs["pk"])

        return queryset.filter(created_at__range=(today_start, today_end))
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field'] = Fields.objects.get(pk = self.kwargs["pk"])

        date_lable = []
        i = 0
        for date in range(7):
            date_lable.append(str(datetime.today() + timedelta(i))[:11])
            i += 1
        
        context['label_data'] = date_lable
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