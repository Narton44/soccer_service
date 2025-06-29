from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class CustomUser(AbstractUser):
    
    objects = UserManager()

    PERMISSIONS = {
        "user": "user",
        "manager": "manager",
        "admin": "admin",
    }

    email = models.EmailField(
        verbose_name="Email", 
        unique=True
        )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=11, 
        unique=True
        )
    
    role = models.CharField(
        verbose_name="Роль пользователя",
        max_length=7,
        choices=PERMISSIONS,
        default="user"  
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



