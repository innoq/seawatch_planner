# Generated by Django 2.2.8 on 2019-12-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0018_auto_20191216_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='issuing_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
