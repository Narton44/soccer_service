from django.db import models
from users.models import CustomUser

class Fields(models.Model):
    """Модель футбольного поля"""

    COVER_CHOICES = [
        ("Резина", "Резина"),
        ("Грунт", "Грунт")
        ]

    adress = models.CharField(
        verbose_name = "Адрес",
        max_length = 50
        )
    
    img = models.ImageField(
        verbose_name = "Картинка поля",
        upload_to="img/",
        blank=True,
        null=True
    )
    
    description = models.TextField(
        verbose_name="Описание поля",
        blank=True,
        null=True
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
