from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone or not password:
            raise ValueError("phone number and password are required fields.")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(phone, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, max_length=20)
    phone_history = models.JSONField(default=dict)
    phone_verified = models.BooleanField(default=False)

    email = models.EmailField(max_length=254, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomBaseUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []