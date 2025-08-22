from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class Booking(models.Model):
    """Модель брони футбольного поля"""
    
    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждено"),
        ("canceled", "Отменено"),
        ("completed", "Завершено"),
    ]

    field = models.ForeignKey(
        "Fields",
        verbose_name="Футбольное поле",
        on_delete=models.PROTECT,
        related_name="bookings"
    )
    
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="bookings"
    )
    
    date = models.DateField(
        verbose_name="Дата игры"
    )

    start_time = models.TimeField(
        verbose_name="Время начала"
    )
    
    end_time = models.TimeField(
        verbose_name="Время окончания"
    )
    
    status = models.CharField(
        verbose_name="Статус бронирования",
        max_length=100,
        choices=STATUS_CHOICES,
        default="pending"
    )
    
    created_at = models.DateTimeField(
        verbose_name="Дата создания брони",
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления брони",
        auto_now=True
    )

    def __str__(self):
        return f"Бронь #{self.id} - {self.field.adress}"
    
    def clean(self):
        # Проверка, что время окончания позже времени начала
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала")
        
        # Проверка, что бронь делается минимум на 1 час
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = datetime.combine(self.date, self.end_time)
        duration = end_dt - start_dt
        
        if duration.total_seconds() < 3600:
            raise ValidationError("Минимальное время бронирования - 1 час")
        
        # Проверка, что бронь не в прошлом (ИСПРАВЛЕНО - добавляем временную зону)
        booking_datetime = datetime.combine(self.date, self.start_time)
        # Преобразуем наивный datetime в осведомленный (с временной зоной)
        booking_datetime_aware = timezone.make_aware(booking_datetime)
        if booking_datetime_aware < timezone.now():
            raise ValidationError("Нельзя забронировать поле в прошлом")
        
        # Проверка на пересечение с другими бронями (только если у брони есть дата)
        if self.date and self.field:
            overlapping_bookings = Booking.objects.filter(
                field=self.field,
                date=self.date,
                status__in=["pending", "confirmed"]
            ).exclude(
                pk=self.pk if self.pk else None
            ).filter(
                # Условие пересечения временных интервалов
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            
            if overlapping_bookings.exists():
                raise ValidationError("Это время уже занято другой бронировкой")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)
    
    @property
    def duration(self):
        """Возвращает продолжительность брони в часах"""
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = datetime.combine(self.date, self.end_time)
        return (end_dt - start_dt).total_seconds() / 3600
    
    @property
    def start_datetime(self):
        """Возвращает datetime начала брони с временной зоной"""
        naive_datetime = datetime.combine(self.date, self.start_time)
        return timezone.make_aware(naive_datetime)
    
    @property
    def end_datetime(self):
        """Возвращает datetime окончания брони с временной зоной"""
        naive_datetime = datetime.combine(self.date, self.end_time)
        return timezone.make_aware(naive_datetime)
    
    @property
    def is_past(self):
        """Проверяет, прошла ли уже бронь"""
        return self.start_datetime < timezone.now()
    
    @classmethod
    def is_time_slot_available(cls, field, date, start_time, end_time, exclude_booking_id=None):
        """
        Проверяет, свободен ли временной интервал
        """
        overlapping_bookings = cls.objects.filter(
            field=field,
            date=date,
            status__in=["pending", "confirmed"]
        ).exclude(
            pk=exclude_booking_id
        ).filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        return not overlapping_bookings.exists()
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date", "start_time"]