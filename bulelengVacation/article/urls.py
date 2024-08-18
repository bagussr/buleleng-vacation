from django.urls import path

from article import views

urlpatterns = [
    path("", views.artikel, name="artikel"),
    path("add", views.AddArtikelView.as_view(), name="add_artikel"),
    path("<str:judul>", views.artikel_detail),
    path("delete/<int:id>", views.delete_artikel, name="delete_artikel"),
    path("edit/<int:id>", views.EditArtikelView.as_view(), name="edit_artikel"),
    path("detail/<int:id>", views.detail_artikel, name="detail_artikel"),
]
