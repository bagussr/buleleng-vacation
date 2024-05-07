from django.db import models

from auths.models import CustomUser

# Create your models here.


class Kategori(models.Model):
    nama = models.CharField(max_length=255)


class Wisata(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    deskripsi = models.TextField()
    perizinan = models.ImageField(upload_to="wisata/izin", null=True, blank=True)
    gambar_utama = models.ImageField(upload_to="wisata", null=True, blank=True)

    def convert(self):
        rating = self.feedback_set.all()
        print(rating)
        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "deskripsi": self.deskripsi,
            "perizinan": self.perizinan,
            "gambar_utama": self.gambar_utama,
            "kategori": self.kategoriwisata_set.first().kategori_id.nama,
            "rating": rating,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "deskripsi": self.deskripsi,
            "kategori": self.kategoriwisata_set.first().kategori_id.id,
        }


class KategoriWisata(models.Model):
    kategori_id = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    wisata_id = models.ForeignKey(Wisata, on_delete=models.CASCADE)


class FotoWisata(models.Model):
    foto = models.ImageField(upload_to="wisata/gambar")
    main = models.BooleanField(default=False)

    wisata_id = models.ForeignKey(Wisata, on_delete=models.CASCADE)


class Feedback(models.Model):
    text = models.TextField()
    rating = models.FloatField()
    tanggal = models.DateTimeField(auto_now_add=True)

    wisata_id = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
