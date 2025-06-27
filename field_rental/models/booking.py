from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone


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
    
    start_time = models.DateTimeField(
        verbose_name="Время начала"
    )
    
    end_time = models.DateTimeField(
        verbose_name="Время окончания"
    )
    
    status = models.CharField(
        verbose_name="Статус бронирования",
        max_length=10,
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
        return f"Бронь #{self.id} - {self.field.adress} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"
    
    def clean(self):
        # Проверка, что время окончания позже времени начала
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала")
        
        # Проверка, что бронь делается минимум на 1 час
        if (self.end_time - self.start_time).total_seconds() < 3600:
            raise ValidationError("Минимальное время бронирования - 1 час")
        
        # Проверка, что бронь не в прошлом
        if self.start_time < timezone.now():
            raise ValidationError("Нельзя забронировать поле в прошлом")
        
        # Проверка на пересечение с другими бронями
        overlapping_bookings = Booking.objects.filter(
            field=self.field,
            status__in=["pending", "confirmed"],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        
        if overlapping_bookings.exists():
            raise ValidationError("Это время уже занято другой бронировкой")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-start_time"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name="end_time_after_start_time"
            ),
            models.UniqueConstraint(
                fields=['field', 'start_time', 'end_time'],
                condition=models.Q(status__in=['pending', 'confirmed']),
                name='unique_booking_slot'
            )
        ]