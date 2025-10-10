from django.shortcuts import get_object_or_404, redirect
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
from django.contrib import messages
from django.db.models import Q



from ..models import Booking, Fields
from ..forms import BookingForm
from ..mixins import AccessMixin


# Booking views

class BookingsCreateView(AccessMixin, CreateView):
    allowed_roles = ["manager", "admin", "user"]

    model = Booking
    template_name = "bookings/bookingcreate.html"
    form_class = BookingForm
    success_url = reverse_lazy("bookings:bookinglist")

class BookingsListView(AccessMixin, ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookings/bookinglist.html"
    allowed_roles = ["manager", "admin", "user"]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start')
        duration_str = request.POST.get('duration')

        try:
            # Получаем поле
            field = get_object_or_404(Fields, pk=self.kwargs["pk"])
            
            # Преобразуем данные
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            duration = int(duration_str)

            # Проверяем валидность продолжительности
            if duration <= 0:
                messages.error(request, "Продолжительность должна быть положительным числом")
                return redirect('bookings', self.kwargs["pk"])

            # Вычисляем время окончания через datetime объекты
            start_datetime = datetime.combine(date, start_time)
            end_datetime = start_datetime + timedelta(hours=duration)
            end_time = end_datetime.time()

            # Проверяем, не прошла ли дата
            if date < timezone.now().date():
                messages.warning(request, "Нельзя создать бронь на прошедшую дату")
                return redirect('bookings', self.kwargs["pk"])

            # Проверяем, не в прошлом ли время для сегодняшней даты
            if date == timezone.now().date():
                current_time = timezone.now().time()
                if start_time < current_time:
                    messages.warning(request, "Нельзя создать бронь на прошедшее время")
                    return redirect('bookings', self.kwargs["pk"])

            # Проверяем доступность времени
            is_available = self.is_time_slot_available(
                field=field,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            
            if not is_available:
                messages.warning(request, "Это время уже занято. Пожалуйста, выберите другое время.")
                return redirect('bookings', self.kwargs["pk"])

            # Проверяем минимальную продолжительность
            start_dt = datetime.combine(date, start_time)
            end_dt = datetime.combine(date, end_time)
            if (end_dt - start_dt).total_seconds() < 3600:
                messages.error(request, "Минимальное время бронирования - 1 час")
                return redirect('bookings', self.kwargs["pk"])

            # Создаем запись бронирования
            booking = Booking.objects.create(
                field=field,
                user=request.user,
                date=date,
                start_time=start_time,
                end_time=end_time,
                status="pending"  # Используем значение из БД, а не отображаемое
            )
            
            messages.info(request, "Бронь успешно создана! Ожидайте подтверждения.")
            return redirect('bookings', self.kwargs["pk"])
        
        except ValueError as e:
            print(f"Ошибка преобразования данных: {e}")
            messages.error(request, "Неверный формат данных. Проверьте введенные значения.")
            return redirect('bookings', self.kwargs["pk"])
        except Exception as e:
            print(f"Ошибка: {e}")
            messages.error(request, f"Произошла ошибка при создании брони")
            return redirect('bookings', self.kwargs["pk"])

    def is_time_slot_available(self, field, date, start_time, end_time):
        """
        Проверяет, свободен ли временной интервал
        """
        # Ищем пересекающиеся брони
        overlapping_bookings = Booking.objects.filter(
            field=field,
            date=date,
            status__in=["pending", "confirmed"]  # Используем значения из БД
        ).filter(
            # Условие пересечения временных интервалов
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        return not overlapping_bookings.exists()

    def get_queryset(self):
        return Booking.objects.filter(
            field__pk=self.kwargs["pk"],
            date__gte=timezone.now().date()
        ).exclude(
            status__in=["canceled", "completed"]
        ).order_by("date", "start_time")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field'] = get_object_or_404(Fields, pk=self.kwargs["pk"])
        context['date_now'] = timezone.now()
        
        # Добавляем информацию о доступных временных интервалах
        today = timezone.now().date()
        context['today'] = today
        context['min_date'] = today.strftime("%Y-%m-%d")
        
        return context

class BookingsDetailView(DetailView):
    model = Booking
    context_object_name = "bookingdetail"
    template_name = "bookings/bookingdetail.html"

class BookingsUpdateView(AccessMixin, UpdateView):

    allowed_roles = ["manager", "admin"]

    model = Booking
    form_class = BookingForm
    context_object_name = "bookingupdate"
    template_name = "bookings/bookingupdate.html"
    success_url = reverse_lazy("bookings:bookinglist")

class BookingsDeleteView(AccessMixin, DeleteView):
    allowed_roles = ["manager", "admin"]

    context_object_name = "bookingsdelete"
    model = Booking
    template_name = "bookings/bookingdelete.html"
    success_url = reverse_lazy("bookings:bookinglist")

class UserBookingListView(ListView):

    model = Booking
    template_name = 'bookings/bookinguserlist.html'
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user = self.request.user)
    

class UserBookingConfirmManagerView(ListView):
    model = Booking
    template_name = 'bookings/bookingconfirmlist.html'
    context_object_name = "bookings"
    allowed_roles = ["manager", "admin"]

    def get_queryset(self):
        return Booking.objects.filter(
            field__owner=self.request.user,
            status__in=["pending", "confirmed", "completed"]
    ).order_by('-date', '-start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = Booking.objects.filter(status="confirmed")
        hour = 0
        for booking in bookings:
            print(booking.start_time)
            # Реализовать данный код
        # Достать стоймость
        # Математика
        context["confirmed"] = Booking.objects.filter(status="confirmed")
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get("type") == "confirm":
            id = request.POST.get("id")
            booking = Booking.objects.filter(id=id)
            booking.update(status="confirmed")
            return redirect('userbookingsconfirm')
        elif request.POST.get("type") == "cancel":
            id = request.POST.get("id")
            booking = Booking.objects.filter(id=id)
            booking.update(status="canceled")
            return redirect('userbookingsconfirm')