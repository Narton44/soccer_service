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
            return redirect('login')

        date = request.POST.get('date')
        start_time_str = request.POST.get('start')
        duration = request.POST.get('duration')

        try:
            # Преобразуем строку времени в объект времени
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            
            # Преобразуем в datetime для удобного добавления часов
            start_datetime = datetime.combine(datetime.today(), start_time)
            
            # Добавляем продолжительность
            end_datetime = start_datetime + timedelta(hours=int(duration))
            end_time = end_datetime.time()

            # Создаем запись бронирования
            booking = Booking.objects.create(
                field=Fields.objects.get(pk=self.kwargs["pk"]),
                user=request.user,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
            
            return redirect('bookings', self.kwargs["pk"])
        except Exception as e:
            print(f"Ошибка: {e}")
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