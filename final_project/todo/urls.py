
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("create/add", views.add, name="add"),
    path("active", views.active, name="active"),
    path("complete/<int:task_id>", views.complete, name="complete")
    path("complete")
]
