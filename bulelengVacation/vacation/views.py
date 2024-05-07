from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django import forms
from django.views.generic import CreateView, UpdateView
from django.http.response import JsonResponse

from vacation.models import Wisata, Kategori, KategoriWisata

# Create your views here.


def delete_kategori(request, id):
    kategori = Kategori.objects.get(id=id)
    kategori.delete()
    return redirect("/dashboard/kategori")


def delete_wisata(request, id):
    wisata = Wisata.objects.get(id=id)
    wisata.delete()
    return redirect("/dashboard/wisata")


def detail_wisata(request, id):
    wisata = Wisata.objects.get(id=id)

    return JsonResponse(wisata.to_dict(), safe=False)


class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = "__all__"


class WisataForm(forms.ModelForm):
    class Meta:
        model = Wisata
        fields = "__all__"


class EditWisataForm(forms.ModelForm):
    class Meta:
        model = Wisata
        fields = "__all__"


class AddKategoriView(CreateView):
    model = Kategori
    form_class = KategoriForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        Kategori.objects.create(nama=data["nama"])
        return redirect("/dashboard/kategori")


class EditWisataView(UpdateView):
    name = Wisata
    form_class = EditWisataForm

    def post(self, request: HttpRequest, id, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST

        wisata = Wisata.objects.get(id=id)
        perizinan = (
            request.FILES["perizinan"]
            if "perizinan" in request.FILES
            else wisata.perizinan
        )
        gambar = (
            request.FILES["gambar_utama"]
            if "gambar_utama" in request.FILES
            else wisata.gambar_utama
        )

        wisata.nama = data["nama"]
        wisata.alamat = data["lokasi"]
        wisata.deskripsi = data["deskripsi"]
        wisata.perizinan = perizinan
        wisata.gambar_utama = gambar
        wisata.save()

        wisata_kategori = KategoriWisata.objects.filter(wisata_id=wisata.id).first()
        kategori = Kategori.objects.get(id=data["kategori"])
        wisata_kategori.kategori_id = kategori
        wisata_kategori.save()

        return redirect("/dashboard/wisata")


class AddWisataView(CreateView):
    model = Wisata
    form_class = WisataForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        form = WisataForm(request.POST, request.FILES)
        kategori = Kategori.objects.get(id=int(data["kategori"]))
        if "perizinan" in request.FILES:
            perizinan = request.FILES["perizinan"]
        else:
            perizinan = None
        if "gambar_utama" in request.FILES:
            gambar_utama = request.FILES["gambar_utama"]
        else:
            perizinan = None
        wisata = Wisata.objects.create(
            nama=data["nama"],
            alamat=data["lokasi"],
            deskripsi=data["deskripsi"],
            perizinan=perizinan,
            gambar_utama=gambar_utama,
        )
        KategoriWisata.objects.create(kategori_id=kategori, wisata_id=wisata)
        return redirect("/dashboard/wisata")
