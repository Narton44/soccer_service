from django.db import models
from users.models import CustomUser

class Fields(models.Model):

    COVER_CHOICES = [
        ("Резина", "Резина"),
        ("Грунт", "Грунт")
        ]

    adress = models.CharField(
        verbose_name = "Адрес",
        max_length = 50
        )
    
    cover = models.CharField(
        verbose_name = "Покрытие",
        max_length = 30,
        choices = COVER_CHOICES, 
        )
    
    indoor = models.BooleanField(
        verbose_name="Открытое",
        default=True
        )
    
    price = models.DecimalField(
        verbose_name = "Цена за час",
        max_digits = 6,
        decimal_places=2
        )
    
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец поля",
        on_delete=models.PROTECT
    )


    def __str__(self):
        return self.adress
    
    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Поля"


class Times(models.Model):
    time = models.CharField(
        verbose_name = "Время",
        max_length = 10
        )
    
    def __str__(self):
        return self.time
    
    class Meta:
        verbose_name = "Время"
        verbose_name_plural = "Время"


class Pays(models.Model):
    field = models.ForeignKey(
        Fields, 
        verbose_name = "Поле",
        on_delete = models.PROTECT
        )
    time = models.ForeignKey(
        Times, 
        verbose_name = "Время",
        on_delete = models.PROTECT
        )
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "заказы"