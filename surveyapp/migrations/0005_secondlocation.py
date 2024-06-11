# Generated by Django 5.0.3 on 2024-06-10 18:58

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyapp', '0004_alter_survey_recommend'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('cleanliness', models.IntegerField(null=True)),
                ('politeness', models.IntegerField(null=True)),
                ('food', models.IntegerField(null=True)),
                ('recommend', models.IntegerField(null=True)),
                ('feelings', models.TextField(null=True)),
                ('text', models.TextField(null=True)),
            ],
        ),
    ]
