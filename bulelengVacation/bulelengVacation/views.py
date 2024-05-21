from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from vacation.models import Feedback, Kategori, KategoriWisata, Wisata


def index(request):
    wisata = Wisata.objects.all()
    best = Wisata.objects.first()
    kategori = Kategori.objects.all()
    wisatas = []
    for i in wisata:
        print(i.convert())
        wisatas.append(i.convert())

    return render(
        request, "index.html", {"wisata": wisatas, "best": best, "kategori": kategori}
    )


def profile(request):
    feedback = Feedback.objects.filter(user_id=request.user)
    feed = []
    for i in feedback:

        feed.append(i.convert())
    return render(request, "profile.html", {"user": request.user, "feedback": feed})


def wisata(request):
    data = request.GET
    if data.get("c"):
        kategori_wisata = KategoriWisata.objects.filter(kategori_id__nama=data.get("c"))
        wisatas = Wisata.objects.distinct().filter(
            id__in=[x.wisata_id.id for x in kategori_wisata]
        )
    elif data.get("q"):
        wisatas = Wisata.objects.filter(
            Q(nama__icontains=data.get("q")) | Q(alamat__icontains=data.get("q"))
        )
    else:
        wisatas = Wisata.objects.all()
    wisata_s = []
    for item in wisatas:
        wisata_s.append(item.convert())
    kategori = Kategori.objects.all()
    return render(request, "wisata.html", {"wisata": wisata_s, "kategori": kategori})


def logout_def(request):
    logout(request)
    return redirect("/")
