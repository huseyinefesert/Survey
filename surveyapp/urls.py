from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "surveyapp"
urlpatterns = [
    path("survey_A", views.survey_A, name='survey_A'),
    path("thanks", views.thanks, name='thanks'),
    path("contact/", views.contact, name='contact'),
    path("about/", views.about, name='about'),
    path("login/", views.login_function, name='login'),
    path("location-data/A", views.chart, name='admin_main'),
    path("survey_B", views.survey_B, name='survey_B'),
    path("location-data/B", views.chart_B, name='admin_main2'),
    path("ai-suggestions/A", views.get_advice_A, name='result_A'),
    path("ai-suggestions/B", views.get_advice_B, name='result_B'),
    path("kvkk", views.get_kvkk, name='kvkk'),
]