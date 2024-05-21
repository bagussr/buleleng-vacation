from django.shortcuts import render
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from vacation.models import Wisata, Feedback, Kategori
from auths.models import CustomUser

# Create your views here.


@login_required(login_url="/login")
def dashboard(request):
    return render(request, "dashboard/index.html")


@login_required(login_url="/login")
def user(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
        return render(request, "dashboard/user.html", {"users": users})
    return HttpResponseForbidden("You dont have access to this website")


@login_required(login_url="/login")
def wisata(request):
    if request.user.is_superuser:
        wisata = Wisata.objects.all()
    else:
        wisata = Wisata.objects.filter(user_id=request.user.id)
    kategori = Kategori.objects.all()
    wisatas = []

    for item in wisata:
        wisatas.append(item.convert())

    return render(
        request, "dashboard/wisata.html", {"wisata": wisatas, "kategori": kategori}
    )


@login_required(login_url="/login")
def feedback(request):
    if request.user.is_superuser:
        feedback = Feedback.objects.all()
    else:
        feedback = Feedback.objects.filter(wisata_id__user_id=request.user.id)
    feed = []
    for i in feedback:
        data = i.convert()
        data["user"] = CustomUser.objects.get(id=i.convert().get("user"))

        feed.append(data)
    return render(request, "dashboard/feedback.html", {"feedback": feed})


@login_required(login_url="/login")
def kategori(request):
    kategori = Kategori.objects.all()
    return render(request, "dashboard/kategori.html", {"kategori": kategori})
