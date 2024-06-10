from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re
from collections import Counter


def extract_and_count_numbers(text):
    numbers = re.findall(r'\d+', text)
    numbers = list(map(int,numbers))
    count = Counter(numbers)
    
    feelings_array = [
        count[0], count[1], count[2], count[3], count[4], count[5], count[6], count[7], count[8], count[9]
    ]
    return feelings_array

def chart(request):
    if not request.user.is_authenticated:
        return redirect('surveyapp:login')
    
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

    emotions_instances = models.Survey.objects.all()
    overall_feelings = [0,0,0,0,0,0,0,0,0,0]

    for instance in emotions_instances:
        feelings = extract_and_count_numbers(instance.feelings)
        for i in range(10):
            overall_feelings[i] += feelings[i]

    feelings_array = overall_feelings
    
    recommend1 = models.Survey.objects.all().filter(recommend = 1).count()
    recommend0 = models.Survey.objects.all().filter(recommend = -1).count()
    recommend_1 = models.Survey.objects.all().filter(recommend = 0).count()

    text = models.Survey.objects.all()
    politeness_array = [politeness5, politeness4, politeness3, politeness2, politeness1]
    cleanliness_array = [cleanliness5, cleanliness4, cleanliness3, cleanliness2, cleanliness1]
    food_array = [food5, food4, food3, food2, food1]
    recommend_array = [recommend1, recommend0, recommend_1]

    
    return render(request, 'admin_main.html', {'politeness_array': politeness_array,"cleanliness_array":cleanliness_array,"food_array":food_array,"feelings_array":feelings_array,"recommend_array":recommend_array,"text":text})

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

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def login_function(request):
    if request.user.is_authenticated:
        return redirect("surveyapp:admin_main")
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
                return redirect("surveyapp:admin_main")
            else:
                messages.error(request, "Username or Password does not match...")

    return render(request, "login.html")

