from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from vacation.models import Kategori, KategoriWisata, Wisata


@login_required(login_url="/login")
def index(request):
    wisata = Wisata.objects.all()
    best = Wisata.objects.first()
    kategori = Kategori.objects.all()
    kategori_wisata = KategoriWisata.objects.filter(
        kategori_id__in=[x.id for x in kategori]
    ).distinct("wisata_id")
    print(kategori_wisata)

    return render(request, "index.html", {"wisata": wisata, "best": best})


def wisata(request):
    wisatas = Wisata.objects.all()
    return render(request, "wisata.html", {"wisata": wisatas})


def logout_def(request):
    logout(request)
    return redirect("/")
