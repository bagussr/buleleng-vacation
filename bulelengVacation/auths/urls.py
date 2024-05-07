from django.urls import path

from auths import views


urlpatterns = [
    path("delete/<int:id>", views.delete_user, name="delete_user"),
    path("detail/<int:id>", views.detail_user, name="detail_user"),
    path("edit/<int:id>", views.UpdateUserView.as_view(), name="edit_user"),
    path("add", views.AddUserView.as_view(), name="add_user"),
]
