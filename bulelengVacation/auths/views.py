from typing import Any
from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.http.response import JsonResponse
from django.contrib.auth import login, authenticate, user_login_failed


from auths.models import CustomUser

# Create your views here.


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserFormEdit(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "alamat", "is_staff")


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "alamat",
            "ttl",
        )


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password")


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "register.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        user = CustomUser.objects.create(
            username=data["username"],
            password=data["password"],
            first_name=data["firstname"],
            last_name=data["lastname"],
            email=data["email"],
            ttl=data["ttl"],
            alamat=data["alamat"],
            is_staff=False,
        )
        user.set_password(user.password)
        user.save()
        return redirect("/login")


class LoginView(CreateView):
    model = CustomUser
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("/home")
        else:
            return render(self.template_name)


def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    if user:
        user.delete()
        return redirect(to="/dashboard/pengguna")


def detail_user(request, id):
    user = CustomUser.objects.get(id=id)
    return JsonResponse(user.to_dict(), safe=False)


class AddUserView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    success_url = "/dashboard/pengguna"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST

        user = CustomUser.objects.create(
            username=data["username"],
            password=data["password"],
            first_name=data["firstname"],
            last_name=data["lastname"],
            email=data["email"],
            ttl=data["ttl"],
            alamat=data["alamat"],
            is_staff=True if data.get("is_staff") == "on" else False,
        )
        user.set_password(user.password)
        user.save()
        return redirect("/dashboard/pengguna")


class UpdateUserView(UpdateView):
    model = CustomUser
    form_class = CustomUserFormEdit
    success_url = "/dashboard/pengguna"

    def post(self, request: HttpRequest, id, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        user = CustomUser.objects.get(id=id)
        user.first_name = data["firstname"]
        user.last_name = data["lastname"]
        user.alamat = data["alamat"]
        user.email = data["email"]
        user.is_staff = True if data.get("is_staff") == "on" else False
        user.save()
        return redirect("/dashboard/pengguna")
