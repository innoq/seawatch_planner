# Generated by Django 2.2.6 on 2019-10-25 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0008_assessment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
