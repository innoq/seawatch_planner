# Generated by Django 2.2.7 on 2019-11-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0013_auto_20191113_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='approved_positions',
            field=models.ManyToManyField(blank=True, related_name='approved_profiles', to='seawatch_registration.Position'),
        ),
    ]
