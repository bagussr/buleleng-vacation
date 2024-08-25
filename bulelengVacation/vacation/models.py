from datetime import datetime
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
    pilihan = models.BooleanField(default=False)
    no_rek = models.CharField(max_length=100, null=True, blank=True)
    bank = models.CharField(max_length=100, null=True, blank=True)
    biaya = models.CharField(max_length=255, null=True, blank=True)
    high_season = models.BooleanField(default=False)
    show_rating = models.BooleanField(default=False)
    maks = models.IntegerField(default=0)

    kategori = models.ForeignKey(
        Kategori, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )

    def convert(self):
        rating = self.feedback_set.all()
        photos = self.fotowisata_set.all()
        reservasi = self.reservasiwisata_set.filter(hari=datetime.now()).all()
        sold = 0
        for i in reservasi:
            sold += i.jumlah
        rate = 0
        for i in rating:
            rate += round(i.rating / float(self.feedback_set.filter(hide=0).count()), 1)

        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "deskripsi": self.deskripsi,
            "perizinan": self.perizinan,
            "emmet_tag": self.emmet_tags,
            "gambar_utama": self.gambar_utama,
            "kategori": self.kategori.nama if self.kategori else None,
            "rating": rate,
            "pilihan": self.pilihan,
            "gambar_lain": photos,
            "no_rek": self.no_rek,
            "bank": self.bank,
            "biaya": self.biaya,
            "high_season": self.high_season,
            "show_rating": self.show_rating,
            "maks": self.maks,
            "sisa": (self.maks - sold) if (self.maks - sold) > 0 else 0,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "emmet_tag": self.emmet_tags,
            "deskripsi": self.deskripsi,
            "kategori": self.kategori.id if self.kategori else None,
            "pilihan": self.pilihan,
            "no_rek": self.no_rek,
            "bank": self.bank,
            "biaya": self.biaya,
            "high_season": self.high_season,
            "maks": self.maks,
            "show_rating": self.show_rating,
        }


class FotoWisata(models.Model):
    foto = models.ImageField(upload_to="wisata/gambar")
    main = models.BooleanField(default=False)

    wisata_id = models.ForeignKey(Wisata, on_delete=models.CASCADE)


class Feedback(models.Model):
    text = models.TextField()
    rating = models.FloatField()
    tanggal = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)

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
            "hide": self.hide,
        }


class VacationAnalytic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wisata = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class TravelAgency(models.Model):
    nama = models.CharField(max_length=255)
    kontak = models.CharField(max_length=100)
    alamat = models.TextField()
    deskripsi = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="agency/")
    website = models.TextField(null=True, blank=True)
    is_hotel = models.BooleanField(default=False)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )


class WisataAgency(models.Model):
    wisata = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE)


class LoginWisataAnalytic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wisata = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)


class ReportWisata(models.Model):
    kunjungan = models.IntegerField(default=0, null=False, blank=False)
    tanggal = models.DateField(null=True, blank=True)
    wisata = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)


class ReservasiWisata(models.Model):
    pembayaran = models.ImageField(
        upload_to="wisata/pemabayaran", null=True, blank=True
    )
    fullpayment = models.BooleanField(default=False)
    nama = models.CharField(max_length=255)
    no_wa = models.CharField(max_length=15)
    hari = models.DateField()
    jumlah = models.IntegerField()
    wisata = models.ForeignKey(Wisata, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)


class KritikSaran(models.Model):
    text = models.TextField()

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)


class Information(models.Model):
    gambar_utama = models.ImageField(upload_to="information", null=True, blank=True)
