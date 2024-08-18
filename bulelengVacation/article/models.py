from django.db import models

# Create your models here.


class Article(models.Model):
    judul = models.CharField(max_length=255)
    gambar = models.ImageField(upload_to="article/")
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def convert(self):
        return {
            "judul": self.judul,
            "gambar": self.gambar.url,
            "content": self.content,
            "created_at": self.created_at,
        }
