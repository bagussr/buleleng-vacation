from django.db import models

from auths.models import CustomUser

# Create your models here.


class Kategori(models.Model):
    nama = models.CharField(max_length=255)


class Wisata(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.TextField()
    emmet_tags = models.TextField()
    deskripsi = models.TextField()
    perizinan = models.ImageField(upload_to="wisata/izin", null=True, blank=True)
    gambar_utama = models.ImageField(upload_to="wisata", null=True, blank=True)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )

    def convert(self):
        rating = self.feedback_set.all()
        photos = self.fotowisata_set.all()
        rate = 0
        for i in rating:
            rate += i.rating / float(self.feedback_set.count())

        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "deskripsi": self.deskripsi,
            "perizinan": self.perizinan,
            "emmet_tag": self.emmet_tags,
            "gambar_utama": self.gambar_utama,
            "kategori": self.kategoriwisata_set.first().kategori_id.nama,
            "rating": rate,
            "gambar_lain": photos,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "emmet_tag": self.emmet_tags,
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

    def convert(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "range": list(range(int(self.rating))),
            "tanggal": self.tanggal,
            "user": self.user_id_id,
            "wisata": self.wisata_id,
        }
