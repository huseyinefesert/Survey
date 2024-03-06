from django.urls import path
from . import views
app_name = "surveyapp"
urlpatterns = [
    path("", views.index, name='index'),
    #path("home", views.home, name='home'),
    path("survey", views.checkboxes, name='home'),
    path("thanks", views.thanks, name='thanks'),
    path("adminsite/", views.adminsite, name='adminsite'),
    path("contact/", views.contact, name='contact'),
    path("about/", views.about, name='about'),
]