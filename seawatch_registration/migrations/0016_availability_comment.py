# Generated by Django 2.2.7 on 2019-12-02 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0015_delete_assessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
