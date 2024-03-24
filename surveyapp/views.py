from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def chart(request):
    politeness5 = models.Survey.objects.all().filter(politeness = 5).count()
    politeness4 = models.Survey.objects.all().filter(politeness = 4).count()
    politeness3 = models.Survey.objects.all().filter(politeness = 3).count()
    politeness2 = models.Survey.objects.all().filter(politeness = 2).count()
    politeness1 = models.Survey.objects.all().filter(politeness = 1).count()

    cleanliness5 = models.Survey.objects.all().filter(cleanliness = 5).count()
    cleanliness4 = models.Survey.objects.all().filter(cleanliness = 4).count()
    cleanliness3 = models.Survey.objects.all().filter(cleanliness = 3).count()
    cleanliness2 = models.Survey.objects.all().filter(cleanliness = 2).count()
    cleanliness1 = models.Survey.objects.all().filter(cleanliness = 1).count()

    food5 = models.Survey.objects.all().filter(food = 5).count()
    food4 = models.Survey.objects.all().filter(food = 4).count()
    food3 = models.Survey.objects.all().filter(food = 3).count()
    food2 = models.Survey.objects.all().filter(food = 2).count()
    food1 = models.Survey.objects.all().filter(food = 1).count()

    happy = models.Survey.objects.all().filter(feelings = 0).count()
    happy2 = models.Survey.objects.all().filter(feelings = 1).count()
    happy3 = models.Survey.objects.all().filter(feelings = 2).count()
    happy4 = models.Survey.objects.all().filter(feelings = 3).count()
    happy5 = models.Survey.objects.all().filter(feelings = 4).count()
    happy6 = models.Survey.objects.all().filter(feelings = 5).count()
    happy7 = models.Survey.objects.all().filter(feelings = 6).count()
    happy8 = models.Survey.objects.all().filter(feelings = 7).count()
    happy9 = models.Survey.objects.all().filter(feelings = 8).count()
    happy0 = models.Survey.objects.all().filter(feelings = 9).count()
    recommend1 = models.Survey.objects.all().filter(recommend = 1).count()
    recommend0 = models.Survey.objects.all().filter(recommend = 0).count()
    #recommend_1 = models.Survey.objects.all().filter(recommend = -1).count()

    text = models.Survey.objects.all()
    politeness_array = [politeness5, politeness4, politeness3, politeness2, politeness1]
    cleanliness_array = [cleanliness5, cleanliness4, cleanliness3, cleanliness2, cleanliness1]
    food_array = [food5, food4, food3, food2, food1]
    feelings_array = [happy, happy2, happy3, happy4, happy5, happy6, happy7, happy8, happy9, happy0]
    recommend_array = [recommend1, recommend0 ]

    
    return render(request, 'test.html', {'politeness_array': politeness_array,"cleanliness_array":cleanliness_array,"food_array":food_array,"feelings_array":feelings_array,"recommend_array":recommend_array,"text":text})

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

