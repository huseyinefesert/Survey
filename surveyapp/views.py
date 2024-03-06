from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#def home(request):
#    return render(request, 'mainpage.html')

def checkboxes(request):
    choices = ["Happy", "Joyful", "Excited", "Relaxed", "Amused", "Sadness", "React", "Frustration", "Disappointment", "Irritation"]
    if request.method == "POST":
        result = request.POST.getlist("inp")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        clean = request.POST.get("rateClean")
        polite = request.POST.get("ratePolite")
        food = request.POST.get("rateFood")
        recommed = request.POST.get("recommed")
        comment = request.POST.get("comment")
        models.Survey.objects.create(name = name, email = email, phone = phone, cleanliness = clean, politeness = polite, food = food, recommend = recommed, feelings = result, text = comment)
        return redirect("surveyapp:thanks")
    return render(request, 'mainpage.html')

def thanks(request):
    return render(request, 'thanks.html')

def adminsite(request):
    return render(request, 'adminsite.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def login_function(request):
    if request.user.is_authenticated:
        return redirect("surveyapp:adminsite")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, "User Not Found....")
                return redirect("surveyapp:login")

            if user is not None:
                login(request, user)
                return redirect("surveyapp:adminsite")
            else:
                messages.error(request, "Username or Password does not match...")

    return render(request, "login.html")