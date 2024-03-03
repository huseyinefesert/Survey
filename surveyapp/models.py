from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Survey(models.Model):
    name = models.TextField(null = True)
    email = models.EmailField(null = True)
    phone = PhoneNumberField(blank = False,null = False)
    cleanliness = models.IntegerField(null = True)
    politeness = models.IntegerField(null = True)
    food = models.IntegerField(null = True)
    recommend = models.BooleanField(null = True)
    feelings = models.TextField(null = True)
    text = models.TextField(null = True)