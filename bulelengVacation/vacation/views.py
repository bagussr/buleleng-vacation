from typing import Any
from django import forms
from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.http.response import JsonResponse, HttpResponseRedirect

from auths.models import CustomUser
from vacation.models import (
    Feedback,
    LoginWisataAnalytic,
    ReportWisata,
    ReservasiWisata,
    TravelAgency,
    Wisata,
    Kategori,
    FotoWisata,
    WisataAgency,
    Information,
)

# Create your views here.


def delete_informasi(request, id):
    informasi = Information.objects.get(pk=id)
    informasi.delete()
    return redirect("/dashboard/informasi")


def add_report(request: HttpRequest):
    if request.method.upper() == "POST":
        data = request.POST
        wisata = Wisata.objects.get(pk=data["wisata"])
        ReportWisata.objects.create(
            wisata=wisata, kunjungan=int(data["kunjungan"]), tanggal=data["tanggal"]
        )
        return HttpResponseRedirect("/dashboard/report")
    return HttpResponseRedirect("/dashboard/report")


def reassign_user_travel(request: HttpRequest, id: str):
    travel = TravelAgency.objects.get(pk=id)
    user = CustomUser.objects.get(pk=travel.user.id)
    user.is_agency = False
    user.save()
    travel.user = None
    travel.save()
    return redirect("/dashboard/travel")


def assign_user_travel(request: HttpRequest):
    if request.method.upper() == "POST":
        data = request.POST
        user = CustomUser.objects.filter(id=data["user"]).first()
        user.is_agency = True
        user.save()
        agency = TravelAgency.objects.filter(id=data["travel_id"]).first()
        agency.user = user
        agency.save()
        return HttpResponseRedirect("/dashboard/travel")
    return HttpResponseRedirect("/dashboard/travel")


def rekomendation_vacation(request, id):
    wisata = Wisata.objects.get(id=id)
    wisata.pilihan = False if wisata.pilihan else True
    wisata.save()
    return redirect("/dashboard/wisata")


def delete_agency(request, id):
    wisata_agency = WisataAgency.objects.filter(agency_id=id).all()
    for i in wisata_agency:
        i.delete()
    agency = TravelAgency.objects.get(id=id)
    agency.delete()
    return redirect("/dashboard/travel")


def delete_kategori(request, id):
    kategori = Kategori.objects.get(id=id)
    kategori.delete()
    return redirect("/dashboard/kategori")


def delete_wisata(request, id):
    wisata = Wisata.objects.get(id=id)
    wisata.delete()
    return redirect("/dashboard/wisata")


def detail_wisata_query(request, name):
    wisata = Wisata.objects.filter(nama=name).get()
    feedback = Feedback.objects.filter(wisata_id=wisata).all()
    wisata_agency = WisataAgency.objects.filter(wisata_id=wisata.id).all()
    feed = []
    for i in feedback:
        data = i.convert()
        data["user"] = CustomUser.objects.get(id=i.convert().get("user"))
        feed.append(data)
    agency = TravelAgency.objects.filter(id__in=[x.agency_id for x in wisata_agency])
    if request.user.__str__() != "AnonymousUser":
        LoginWisataAnalytic.objects.create(user=request.user, wisata=wisata)
    return render(
        request,
        "detail_wisata.html",
        {"wisata": wisata.convert(), "feedback": feed, "agency": agency},
    )


def add_more_photo(request):
    file = request.FILES.getlist("gambar_tambahan")
    id = request.POST["id"]
    for item in file:
        FotoWisata.objects.create(wisata_id=Wisata.objects.get(id=id), foto=item)

    return redirect("/dashboard/wisata")


def add_feedback(request):
    data = request.POST
    wisata = Wisata.objects.get(id=data["wisata_id"])
    Feedback.objects.create(
        user_id=request.user,
        text=data["masukan"],
        rating=int(data["rating"]),
        wisata_id=wisata,
    )
    return redirect(data["url"])


def add_agency(request):
    data = request.POST
    _wisata = Wisata.objects.get(id=data.get("wisata_id"))
    for x in data.getlist("agencies[]", []):
        _travel = TravelAgency.objects.get(id=x)
        if (
            WisataAgency.objects.filter(
                agency_id=_travel.id, wisata_id=_wisata.id
            ).count()
            == 0
        ):
            WisataAgency.objects.create(agency=_travel, wisata=_wisata)
    wisata_agency = WisataAgency.objects.filter(wisata_id=_wisata.id).all()

    if len(wisata_agency) > 0:
        for x in wisata_agency:
            if str(x.agency_id) not in data.getlist("agencies[]", []):
                x.delete()
    return redirect("/dashboard/wisata")


def detail_wisata(request, id):
    wisata = Wisata.objects.get(id=id)

    return JsonResponse(wisata.to_dict(), safe=False)


def detail_wisate_agency(request, id):
    wisata_agency = WisataAgency.objects.filter(wisata_id=id)
    return JsonResponse(serializers.serialize("json", wisata_agency), safe=False)


class ReservasiForm(forms.ModelForm):
    class Meta:
        model = ReservasiWisata
        fields = "__all__"


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


class TravelAgencyForm(forms.ModelForm):
    class Meta:
        model = TravelAgency
        fields = "__all__"


class AddIformasiForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = "__all__"


class AddInformasi(CreateView):
    model = Information
    form_class = AddIformasiForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        Information.objects.create(gambar_utama=request.FILES["gambar_utama"])
        return redirect("/dashboard/informasi")


class AddReservasi(CreateView):
    model = ReservasiWisata
    form_class = ReservasiForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        wisata = Wisata.objects.filter(id=data["wisata_id"]).first()
        ReservasiWisata.objects.create(
            pembayaran=(request.FILES.get("pembayaran", None)),
            nama=data["nama"],
            no_wa=data["no_wa"],
            hari=data["hari"],
            jumlah=int(data["jumlah"]),
            wisata=wisata,
            user=request.user,
        )
        return redirect(f"/wisata/{wisata.nama}")


class AddTravelAgency(CreateView):
    model = TravelAgency
    form_class = TravelAgencyForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        TravelAgency.objects.create(
            nama=data.get("nama", ""),
            kontak=data.get("kontak", ""),
            alamat=data.get("alamat", ""),
            deskripsi=data.get("deskripsi", None),
            website=data.get("website", None),
            logo=request.FILES["logo"],
        )

        return redirect("/dashboard/travel")


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

        kategori = Kategori.objects.get(id=data["kategori"])
        wisata.nama = data["nama"]
        wisata.alamat = data["lokasi"]
        wisata.deskripsi = data["deskripsi"]
        wisata.emmet_tags = data["emmet_tag"]
        wisata.biaya = data["biaya"]
        wisata.no_rek = data["no_rek"]
        wisata.bank = data["bank"]
        wisata.kategori = kategori
        wisata.perizinan = perizinan
        wisata.gambar_utama = gambar
        wisata.save()

        return redirect("/dashboard/wisata")


class AddWisataView(CreateView):
    model = Wisata
    form_class = WisataForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        kategori = Kategori.objects.get(id=int(data["kategori"]))
        if "perizinan" in request.FILES:
            perizinan = request.FILES["perizinan"]
        else:
            perizinan = None
        if "gambar_utama" in request.FILES:
            gambar_utama = request.FILES["gambar_utama"]
        else:
            perizinan = None
        Wisata.objects.create(
            nama=data["nama"],
            alamat=data["lokasi"],
            deskripsi=data["deskripsi"],
            emmet_tags=data["emmet_tag"],
            no_rek=data["no_rek"],
            biaya=data["biaya"],
            bank=data["bank"],
            perizinan=perizinan,
            gambar_utama=gambar_utama,
            kategori_id=kategori.id,
            user_id=request.user.id,
        )

        return redirect("/dashboard/wisata")
