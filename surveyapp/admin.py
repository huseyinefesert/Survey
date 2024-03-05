from django.contrib import admin
from . import models
# Register your models here.
class SurveyAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Survey,SurveyAdmin)