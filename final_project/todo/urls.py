
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
    path("complete/<int:task_id>", views.complete, name="complete"),
    path("completed", views.completed, name="completed"),
    path("overdue", views.overdue, name="overdue"),
    path("overduetasks", views.overduetasks, name="overduetasks"),
    path("overdue/<int:task_id>", views.overdueupdate, name="overdueupdate"),

]
