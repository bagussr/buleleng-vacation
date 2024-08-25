from django.urls import path

from dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pengguna", views.user, name="pengguna"),
    path("wisata", views.wisata, name="wisata_dashboard"),
    path("feedback", views.feedback, name="feedback"),
    path("kategori", views.kategori, name="kategori"),
    path("akomodasi", views.travel, name="akomodasi"),
    path("artikel", views.artikel, name="artikel"),
    path("kritik", views.kritik_saran, name="kritik_saran"),
    path("report", views.report, name="report"),
    path("informasi", views.informasi, name="informasi"),
    path("reservasi", views.reservasi, name="reservasi_agency"),
    path("reservasi_wisata", views.reservasi_wisata, name="reservasi_wisata"),
]
