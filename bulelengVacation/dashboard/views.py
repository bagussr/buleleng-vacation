from django.shortcuts import render

from vacation.models import Wisata, Feedback, Kategori
from auths.models import CustomUser

# Create your views here.


def dashboard(request):
    return render(request, "dashboard/index.html")


def user(request):
    users = CustomUser.objects.all()
    return render(request, "dashboard/user.html", {"users": users})


def wisata(request):
    wisata = Wisata.objects.all()
    kategori = Kategori.objects.all()
    wisatas = []

    for item in wisata:
        wisatas.append(item.convert())

    return render(
        request, "dashboard/wisata.html", {"wisata": wisatas, "kategori": kategori}
    )


def feedback(request):
    return render(request, "dashboard/feedback.html")


def kategori(request):
    kategori = Kategori.objects.all()
    return render(request, "dashboard/kategori.html", {"kategori": kategori})
