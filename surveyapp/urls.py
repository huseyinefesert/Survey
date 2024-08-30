from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "surveyapp"
urlpatterns = [
    path("", views.index, name='index'),
    #path("home", views.home, name='home'),
    path("survey_A", views.survey_A, name='survey_A'),
    path("thanks", views.thanks, name='thanks'),
    path("contact/", views.contact, name='contact'),
    path("about/", views.about, name='about'),
    path("login/", views.login_function, name='login'),
    path("admin_page_A/", views.chart, name='admin_main'),
    path("survey_B", views.survey_B, name='survey_B'),
    path("admin_page_B/", views.chart_B, name='admin_main2'),
    path("results_A", views.get_advice_A, name='result_A'),
    path("results_B", views.get_advice_B, name='result_B'),
    path("kvkk", views.get_kvkk, name='kvkk'),
]