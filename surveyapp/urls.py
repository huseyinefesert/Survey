from django.urls import path
from . import views
app_name = "surveyapp"
urlpatterns = [
    path("", views.index, name='index'),
    #path("home", views.home, name='home'),
    path("survey", views.checkboxes, name='home'),
    path("thanks", views.thanks, name='thanks'),
    path("contact/", views.contact, name='contact'),
    path("about/", views.about, name='about'),
    path("login/", views.login_function, name='login'),
    path("admin_main/", views.chart, name='admin_main'),
]