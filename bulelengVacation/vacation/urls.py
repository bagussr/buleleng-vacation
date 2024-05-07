from django.urls import path

from vacation import views

urlpatterns = [
    path("kategori/add", views.AddKategoriView.as_view(), name="add_kategori"),
    path("kategori/delete/<int:id>", views.delete_kategori, name="delete_kategori"),
    path("detail/<int:id>", views.detail_wisata, name="detail_wisata"),
    path("add", views.AddWisataView.as_view(), name="add_wisata"),
    path("delete/<int:id>", views.delete_wisata, name="delete_wisata"),
    path("edit/<int:id>", views.EditWisataView.as_view(), name="edit_wisata"),
]
