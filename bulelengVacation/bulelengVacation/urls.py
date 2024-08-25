"""
URL configuration for bulelengVacation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from auths.views import LoginView, RegisterView

urlpatterns = [
    path("dashboard/", include("dashboard.urls")),
    path("users/", include("auths.urls")),
    path("wisata/", include("vacation.urls")),
    path("artikel/", include("article.urls")),
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("", views.index, name="index"),
    path("akomodasi", views.agensi, name="akomodasi"),
    path("hotel", views.hotel, name="hotel"),
    path(
        "akomodasi/<str:nama>",
        views.detail_agensi,
    ),
    path(
        "hotel/<str:nama>",
        views.detail_agensi,
    ),
    path("kritik", views.kritik_saran, name="kritik"),
    path("wisata", views.wisata, name="wisata"),
    path("home", views.index, name="index"),
    path("logout", views.logout_def, name="logout"),
    path("profile", views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
