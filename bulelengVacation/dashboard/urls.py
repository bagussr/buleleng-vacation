from django.urls import path

from dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pengguna", views.user, name="pengguna"),
    path("wisata", views.wisata, name="wisata_dashboard"),
    path("feedback", views.feedback, name="feedback"),
    path("kategori", views.kategori, name="kategori"),
    path("travel", views.travel, name="travel"),
]
