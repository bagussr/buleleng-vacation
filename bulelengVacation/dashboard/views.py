from django import template
from django.core import serializers
from django.shortcuts import render
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from vacation.models import (
    TravelAgency,
    Wisata,
    Feedback,
    Kategori,
    LoginWisataAnalytic,
)
from auths.models import CustomUser

# Create your views here.

register = template.Library()


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(",")


@login_required(login_url="/login")
def dashboard(request):
    if request.user.is_superuser:
        res = (
            LoginWisataAnalytic.objects.values("wisata_id")
            .annotate(dcount=Count("wisata_id"))
            .order_by()
        )
    else:
        wisata = Wisata.objects.filter(user_id=request.user.id)
        res = (
            LoginWisataAnalytic.objects.values("wisata_id")
            .annotate(dcount=Count("wisata_id"))
            .filter(wisata_id__in=[x.id for x in wisata])
            .order_by()
        )
    analytic = []
    for x in res:
        analytic.append(
            {
                "wisata": Wisata.objects.get(pk=x["wisata_id"]).nama,
                "dcount": x["dcount"],
            }
        )
    return render(request, "dashboard/index.html", {"analytic": analytic})


@login_required(login_url="/login")
def travel(request):
    agencies = TravelAgency.objects.all()
    return render(request, "dashboard/agency.html", {"agencies": agencies})


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
    agencies = TravelAgency.objects.all()

    for item in wisata:
        wisatas.append(item.convert())

    return render(
        request,
        "dashboard/wisata.html",
        {
            "wisata": wisatas,
            "kategori": kategori,
            "agencies": agencies,
            "x": serializers.serialize("json", agencies),
        },
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
