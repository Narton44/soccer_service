from django.shortcuts import redirect
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
    
    # Переписать добавленние брони сделать систему уведомлений!
    def post(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # или другая страница

            date = request.POST.get('date')
            start_time = request.POST.get('start')
            duration = request.POST.get('duration')

            if not all([date, start_time, duration]):
                return redirect('bookings', self.kwargs["pk"])  # имя URL вашей формы

            try:
                # Создаем запись бронирования
                booking = Booking.objects.create(
                    field = Fields.objects.get(pk = self.kwargs["pk"]),
                    user=request.user,
                    start_time=date,
                    end_time=start_time + int(duration),
                    
                )
                return redirect('bookings', self.kwargs["pk"])  # перенаправляем на список бронирований
            except Exception as e:
                return redirect('bookings', self.kwargs["pk"])

    def get_queryset(self):

        return Booking.objects.filter(field__pk = self.kwargs["pk"])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field'] = Fields.objects.get(pk = self.kwargs["pk"])

        date_now = timezone.now()
        
        context['date_now'] = date_now
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