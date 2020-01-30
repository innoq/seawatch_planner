# Generated by Django 2.2.7 on 2020-01-27 17:41

import django_countries.fields
from django.db import migrations

import seawatch_registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0025_merge_20200127_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='citizenship',
            field=django_countries.fields.CountryField(countries=seawatch_registration.models.Nationalities, max_length=746, multiple=True, verbose_name='Citizenship'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country_of_birth',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country of birth'),
        ),
    ]