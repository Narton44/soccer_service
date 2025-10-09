from django.db import models
from users.models import CustomUser


class Cover(models.Model):
    name = models.CharField(
        verbose_name="Название покрытия",
        max_length=50
    )
    slug = models.SlugField(
        verbose_name="Сылка",
        unique=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Покрытие"
        verbose_name_plural = "Покрытия"

class IndoorSign(models.Model):
    name = models.CharField(
        verbose_name="Признак крытое/нет",
        max_length=10,
        default='unknown'
    )
    slug = models.SlugField(
        verbose_name="Сылка/крыт",
        unique=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Признак крытое/нет"

class Fields(models.Model):
    """Модель футбольного поля"""

    adress = models.CharField(
        verbose_name = "Адрес",
        max_length = 50
        )
    
    phone_number = models.CharField(
        verbose_name = "телефон",
        max_length = 12,
        default=None
        )
    
    opening_hours = models.CharField(
        verbose_name = "время работы",
        max_length = 12,
        default=None
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

    cover = models.ForeignKey(
        Cover,
        on_delete=models.PROTECT,
        verbose_name="Покрытие"
    )

    indoorsign = models.ForeignKey(
        IndoorSign,
        on_delete=models.PROTECT,
        verbose_name="Признак крытое/нет"
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

