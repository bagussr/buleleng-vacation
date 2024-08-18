from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from article.models import Article
from vacation.models import (
    Feedback,
    Information,
    Kategori,
    KritikSaran,
    TravelAgency,
    Wisata,
)


@login_required(login_url="/login")
def kritik_saran(request: HttpRequest):
    if request.method.upper() == "POST":
        KritikSaran.objects.create(text=request.POST["text"], user=request.user)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return redirect(request.META.get("HTTP_REFERER"))


def index(request):
    wisata = Wisata.objects.exclude(pilihan=False).order_by("-id").all()
    best = Wisata.objects.first()
    kategori = Kategori.objects.all()
    agency = TravelAgency.objects.order_by("-id").all()
    artikel = Article.objects.order_by("-id").all()
    information = Information.objects.all()
    wisatas = []
    for i in wisata:
        wisatas.append(i.convert())

    return render(
        request,
        "index.html",
        {
            "wisata": wisatas[:3],
            "best": best,
            "kategori": kategori,
            "agency": agency[:3],
            "artikel": artikel,
            "information": information,
        },
    )


@login_required(login_url="/login")
def profile(request):
    feedback = Feedback.objects.filter(user_id=request.user)
    feed = []
    agency = TravelAgency.objects.all()
    for i in feedback:

        feed.append(i.convert())
    return render(
        request,
        "profile.html",
        {
            "user": request.user,
            "feedback": feed,
            "agency": agency,
        },
    )


def wisata(request):
    data = request.GET
    agency = TravelAgency.objects.all()

    if data.get("c"):
        kategori = Kategori.objects.filter(nama=data.get("c"))
        wisatas = (
            Wisata.objects.exclude(pilihan=False)
            .distinct()
            .filter(kategori__in=[x.id for x in kategori])
        )
    elif data.get("q"):
        wisatas = Wisata.objects.filter(
            Q(nama__icontains=data.get("q")) | Q(alamat__icontains=data.get("q"))
        ).exclude(pilihan=False)
    else:
        wisatas = Wisata.objects.exclude(pilihan=False).all()
    wisata_s = []
    for item in wisatas:
        wisata_s.append(item.convert())
    kategori = Kategori.objects.all()
    return render(
        request,
        "wisata.html",
        {
            "wisata": wisata_s,
            "kategori": kategori,
            "agency": agency,
        },
    )


def agensi(request):
    agency = TravelAgency.objects.all()

    return render(request, "agency.html", {"agensi": agency})


def detail_agensi(request, nama):
    agency = TravelAgency.objects.filter(nama=nama).first()

    return render(request, "detail_agency.html", {"agensi": agency})


def logout_def(request):
    logout(request)
    return redirect("/")
