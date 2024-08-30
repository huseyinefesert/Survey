from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Avg
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
import re
from collections import Counter
import google.generativeai as genai

genai.configure(api_key='AIzaSyDGap4WpwiUiMEIQOg6-1ilyWsXTCyduD4')
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def get_kvkk(request):
    return render(request,"kvkk.html")

def get_advice_A(request):
    if not request.user.is_authenticated:
        return redirect('surveyapp:login')

    response = generate_advice("A")

    response = response.replace("**", "")
    response = response.replace(":", ":<br>")
    response = response.replace("-", "<br>-")

    for i in range(1,10):
        response = response.replace(str(i)+".", "<br><br>"+str(i)+".")

    return render(request, "result_A.html", {"advice": response})

def get_advice_B(request):
    if not request.user.is_authenticated:
        return redirect('surveyapp:login')

    response = generate_advice("B")

    response = response.replace("**", "")
    response = response.replace(":", ":<br>")
    response = response.replace("-", "<br>-")

    for i in range(1,10):
        response = response.replace(str(i)+".", "<br><br>"+str(i)+".")

    return render(request, "result_B.html", {"advice": response})

def generate_advice(location):

    match location:
        case "A":
            data = calculate_averages(models.Survey.objects.using("default"), location)
            prompt = "Görevlilerin tutumunun ortalama puanı {0:.2f}, Temizlik ortalama puanı {1:.2f}, Yiyeceklerin kalitesi ortalama puanı {2:.2f}, Tavsiye etme ortalama puanı {3:.2f}. Verilere dayanarak hizmetimizi geliştirmek için ne yapabiliriz? (Numaralandarılmış şekilde ve '-' kullanarak yaz.Ayrıca puan ortalamalarını virgül ile yaz nokta ile DEĞİL.)".format(
                data['avg_politeness'],
                data['avg_cleanliness'],
                data['avg_food'],
                data['avg_recommend']
            )
        case "B":
            data = calculate_averages(models.Survey_B.objects.using("second_db"), location)
            prompt = "Görevlilerin tutumunun ortalama puanı {0:.2f}, Temizlik ortalama puanı {1:.2f}, Havalandırma kalitesi ortalama puanı {2:.2f}, Tavsiye etme ortalama puanı {3:.2f}. Verilere dayanarak hizmetimizi geliştirmek için ne yapabiliriz? (Numaralandarılmış şekilde ve '-' kullanarak yaz.Ayrıca puan ortalamalarını virgül ile yaz nokta ile DEĞİL.)".format(
                data['avg_politeness'],
                data['avg_cleanliness'],
                data['avg_vent'],
                data['avg_recommend']
            )
            
    responses = gemini_model.generate_content(prompt)
    return responses.parts[0].text


def calculate_averages(queryset, location):
    match location:
        case "A":
            averages = queryset.aggregate(
            avg_cleanliness = Avg('cleanliness'),
            avg_politeness = Avg('politeness'),
            avg_food = Avg('food'),
            avg_recommend = Avg('recommend')
    )
        case "B":
            averages = queryset.aggregate(
            avg_cleanliness = Avg('cleanliness'),
            avg_politeness = Avg('politeness'),
            avg_vent = Avg('vent'),
            avg_recommend = Avg('recommend')
    )

    return averages

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

    
    politeness5 = models.Survey.objects.using("default").filter(politeness = 5).count()
    politeness4 = models.Survey.objects.using("default").filter(politeness = 4).count()
    politeness3 = models.Survey.objects.using("default").filter(politeness = 3).count()
    politeness2 = models.Survey.objects.using("default").filter(politeness = 2).count()
    politeness1 = models.Survey.objects.using("default").filter(politeness = 1).count()

    cleanliness5 = models.Survey.objects.using("default").filter(cleanliness = 5).count()
    cleanliness4 = models.Survey.objects.using("default").filter(cleanliness = 4).count()
    cleanliness3 = models.Survey.objects.using("default").filter(cleanliness = 3).count()
    cleanliness2 = models.Survey.objects.using("default").filter(cleanliness = 2).count()
    cleanliness1 = models.Survey.objects.using("default").filter(cleanliness = 1).count()

    food5 = models.Survey.objects.using("default").filter(food = 5).count()
    food4 = models.Survey.objects.using("default").filter(food = 4).count()
    food3 = models.Survey.objects.using("default").filter(food = 3).count()
    food2 = models.Survey.objects.using("default").filter(food = 2).count()
    food1 = models.Survey.objects.using("default").filter(food = 1).count()

    emotions_instances = models.Survey.objects.using("default")
    overall_feelings = [0,0,0,0,0,0,0,0,0,0]

    for instance in emotions_instances:
        feelings = extract_and_count_numbers(instance.feelings)
        for i in range(10):
            overall_feelings[i] += feelings[i]

    feelings_array = overall_feelings
    
    recommend5 = models.Survey.objects.using("default").filter(recommend = 5).count()
    recommend3 = models.Survey.objects.using("default").filter(recommend = 3).count()
    recommend1 = models.Survey.objects.using("default").filter(recommend = 1).count()

    text = models.Survey.objects.using("default")
    politeness_array = [politeness5, politeness4, politeness3, politeness2, politeness1]
    cleanliness_array = [cleanliness5, cleanliness4, cleanliness3, cleanliness2, cleanliness1]
    food_array = [food5, food4, food3, food2, food1]
    recommend_array = [recommend5, recommend1, recommend3]

    
    return render(request, 'admin_main.html', {'politeness_array': politeness_array,"cleanliness_array":cleanliness_array,"food_array":food_array,"feelings_array":feelings_array,"recommend_array":recommend_array,"text":text})

def chart_B(request):
    if not request.user.is_authenticated:
        return redirect('surveyapp:login')

    politeness5 = models.Survey_B.objects.using("second_db").filter(politeness = 5).count()
    politeness4 = models.Survey_B.objects.using("second_db").filter(politeness = 4).count()
    politeness3 = models.Survey_B.objects.using("second_db").filter(politeness = 3).count()
    politeness2 = models.Survey_B.objects.using("second_db").filter(politeness = 2).count()
    politeness1 = models.Survey_B.objects.using("second_db").filter(politeness = 1).count()

    cleanliness5 = models.Survey_B.objects.using("second_db").filter(cleanliness = 5).count()
    cleanliness4 = models.Survey_B.objects.using("second_db").filter(cleanliness = 4).count()
    cleanliness3 = models.Survey_B.objects.using("second_db").filter(cleanliness = 3).count()
    cleanliness2 = models.Survey_B.objects.using("second_db").filter(cleanliness = 2).count()
    cleanliness1 = models.Survey_B.objects.using("second_db").filter(cleanliness = 1).count()

    vent5 = models.Survey_B.objects.using("second_db").filter(vent = 5).count()
    vent4 = models.Survey_B.objects.using("second_db").filter(vent = 4).count()
    vent3 = models.Survey_B.objects.using("second_db").filter(vent = 3).count()
    vent2 = models.Survey_B.objects.using("second_db").filter(vent = 2).count()
    vent1 = models.Survey_B.objects.using("second_db").filter(vent = 1).count()

    emotions_instances = models.Survey_B.objects.using("second_db")
    overall_feelings = [0,0,0,0,0,0,0,0,0,0]

    for instance in emotions_instances:
        feelings = extract_and_count_numbers(instance.feelings)
        for i in range(10):
            overall_feelings[i] += feelings[i]

    feelings_array = overall_feelings
    
    recommend5 = models.Survey_B.objects.using("second_db").filter(recommend = 5).count()
    recommend3 = models.Survey_B.objects.using("second_db").filter(recommend = 3).count()
    recommend1 = models.Survey_B.objects.using("second_db").filter(recommend = 1).count()

    text = models.Survey_B.objects.using("second_db")
    politeness_array = [politeness5, politeness4, politeness3, politeness2, politeness1]
    cleanliness_array = [cleanliness5, cleanliness4, cleanliness3, cleanliness2, cleanliness1]
    vent_array = [vent5, vent4, vent3, vent2, vent1]
    recommend_array = [recommend5, recommend1, recommend3]

    
    return render(request, 'admin_main2.html', {'politeness_array': politeness_array,"cleanliness_array":cleanliness_array,"vent_array":vent_array,"feelings_array":feelings_array,"recommend_array":recommend_array,"text":text})

def chart_caller(request):
    chart(request)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#def home(request):
#    return render(request, 'mainpage.html')

def survey_A(request):
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
        models.Survey.objects.using("default").create(name = name, email = email, phone = phone, cleanliness = clean, politeness = polite, food = food, recommend = recommed, feelings = result, text = comment)
        return redirect("surveyapp:thanks")
    return render(request, 'mainpage.html')

def survey_B(request):
    choices = ["Happy", "Joyful", "Excited", "Relaxed", "Amused", "Sadness", "React", "Frustration", "Disappointment", "Irritation"]
    if request.method == "POST":
        result = request.POST.getlist("inp")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        clean = request.POST.get("rateClean")
        polite = request.POST.get("ratePolite")
        vent = request.POST.get("rateVent")
        recommed = request.POST.get("recommed")
        comment = request.POST.get("comment")
        models.Survey_B.objects.using("second_db").create(name = name, email = email, phone = phone, cleanliness = clean, politeness = polite, vent = vent, recommend = recommed, feelings = result, text = comment)
        return redirect("surveyapp:thanks")
    return render(request, 'mainpage2.html')

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

