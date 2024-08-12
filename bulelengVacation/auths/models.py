from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class CustomUser(AbstractUser):
    alamat = models.CharField(max_length=255, null=True, blank=True)
    ttl = models.DateField(verbose_name="Tanggal Lahir", null=True, blank=True)
    domisili = models.CharField(max_length=255, null=True, blank=True)
    is_agency = models.BooleanField(default=False)

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
            "is_agency": self.is_agency,
            "domisili": self.domisili,
        }


class LoginAnalytic(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
