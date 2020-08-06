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
from datetime import tzinfo, timedelta, datetime

from .models import User, Tasks

#return all post here#
def index(request):
    return render(request, "todo/index.html")

@login_required
def active(request):
    #get all the task from model#
    tasks = Tasks.objects.filter(completed=False)
    #return task in order of most upcoming first#
    tasks = tasks.order_by("timeset").all()
    return JsonResponse([task.serialize() for task in tasks], safe=False)

def create(request):
    return render(request, "todo/create.html")

@csrf_exempt
@login_required
def complete(request, task_id):
    task = Tasks.objects.get(
        id = task_id
    )
    if request.method == "PUT":
        data = json.loads(request.body)
        task.completed = data["completed"]
        task.save()
        task.timeset = data["time_set"]
        task.save()
        return JsonResponse({"message": "successfully updated"})   

@login_required
def completed(request):
    #get tasks with completed marked#
    tasks = Tasks.objects.filter(completed=True)
    #order from most upcoming#
    tasks = tasks.order_by("-timeset").all()
    return render(request, "todo/completed.html", {
        "tasks": tasks
    })

def overdue(request):
    return render(request, "todo/overdue.html")

@login_required
def overduetasks(request):
    tasks = Tasks.objects.filter(overdue=True, completed=False)
    tasks = tasks.order_by("-timeset").all()
    return JsonResponse([task.serialize() for task in tasks], safe=False)

@csrf_exempt
@login_required
def overdueupdate(request, task_id):
    task = Tasks.objects.get(
        id = task_id
    )
    if request.method == "PUT":
        data = json.loads(request.body)
        task.overdue = data["overdue"]
        task.save()
        return JsonResponse({"message": "successfully updated"})     

@csrf_exempt
@login_required
def add(request):
    #adding a new task must be via post#
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    #get data from request#
    data = json.loads(request.body)
    content = data.get("content", "")
    year = data.get("year", "")
    month = data.get("month", "")
    date = data.get("date", "")
    hour = data.get("hour", "")
    minute = data.get("minute", "")
    timeset = data.get("date_time", "")

    task = Tasks(
        user=request.user,
        content=content,
        year=year,
        month=month,
        date=date,
        hour=hour,
        minute=minute,
        timeset=timeset,
    )
    task.save()
    return JsonResponse({"message": "Task created successfully.", "timesaved": task.timeset}, status=201)    

def login_view(request):
    if request.method == "POST":
        #Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        #Check if authentication successful
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
        #Ensure password matches confirmation#
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todo/register.html", {
                "message": "Passwords must match."
            })
        #Attempt to create new user
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

