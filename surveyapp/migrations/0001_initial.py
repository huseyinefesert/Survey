# Generated by Django 5.0.2 on 2024-03-03 06:50

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('cleanliness', models.IntegerField()),
                ('politeness', models.IntegerField()),
                ('food', models.IntegerField()),
                ('recommend', models.BooleanField()),
                ('feelings', models.TextField()),
                ('text', models.TextField()),
            ],
        ),
    ]
