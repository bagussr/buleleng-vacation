from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class CustomUser(AbstractUser):
    alamat = models.CharField(max_length=255, null=True, blank=True)
    ttl = models.DateField(verbose_name="Tanggal Lahir", null=True, blank=True)

    objects = UserManager()

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "alamat": self.alamat,
            "is_staff": self.is_staff,
        }
