# Generated by Django 2.2.8 on 2019-12-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0016_availability_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='seawatch_registration.Skill'),
        ),
    ]
