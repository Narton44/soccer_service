from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
            self, 
            email, 
            password=None, 
            **extra_fields
            ):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email=email), 
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(
            self, 
            email, 
            password=None, 
            **extra_fields
            ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self.create_user(email, password, **extra_fields)
