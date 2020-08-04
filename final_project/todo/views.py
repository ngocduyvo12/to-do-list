import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Tasks

#return all post here
def index(request):
    return render(request, "todo/index.html")


def create(request):
    return render(request, "todo/create.html")    

@csrf_exempt
@login_required
def add(request):
    #adding a new task must be via post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    # get data from request
    data = json.loads(request.body)
    content = data.get("content", "")
    year = data.get("year", "")
    month = data.get("month", "")
    date = data.get("date", "")
    hour = data.get("hour", "")
    minute = data.get("minute", "")

    task = Tasks(
        user = request.user,
        content = content,
        year = year,
        month = month,
        date = date,
        hour = hour,
        minute = minute
    )
    task.save()
    return JsonResponse({"message": "Task created successfully."}, status=201)    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todo/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todo/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "todo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todo/register.html")

