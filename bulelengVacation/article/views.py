from typing import Any
from django.shortcuts import render
from django import forms
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView

from article.models import Article

# Create your views here.


def artikel(request):
    _artikel = Article.objects.all()

    return render(request, "article.html", {"artikel": _artikel})


def artikel_detail(request, judul):
    _artikel = Article.objects.filter(judul=judul).first()
    artikels = Article.objects.exclude(id=_artikel.id).all()

    return render(
        request, "detail_article.html", {"artikel": _artikel, "artikels": artikels[:3]}
    )


def detail_artikel(request, id):
    _artikel = Article.objects.filter(id=id).first()

    return JsonResponse(data=_artikel.convert())


def delete_artikel(request, id):
    _artikel = Article.objects.filter(id=id).first()
    _artikel.delete()
    return redirect("/dashboard/artikel")


class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"


class EditArtikelView(UpdateView):
    model = Article
    form_class = ArtikelForm

    def post(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        data = request.POST
        _artikel = Article.objects.filter(id=id).first()

        gambar = (
            request.FILES["gambar"] if "gambar" in request.FILES else _artikel.gambar
        )

        _artikel.judul = data["judul"]
        _artikel.content = data["content"]
        _artikel.gambar = gambar

        _artikel.save()
        return redirect("/dashboard/artikel")


class AddArtikelView(CreateView):
    model = Article
    form_class = ArtikelForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        Article.objects.create(
            judul=data["judul"], content=data["text"], gambar=request.FILES["gambar"]
        )
        return redirect("/dashboard/artikel")
