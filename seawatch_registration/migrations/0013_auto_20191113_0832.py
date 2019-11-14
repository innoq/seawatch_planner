# Generated by Django 2.2.7 on 2019-11-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0012_auto_20191113_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='approved_profiles',
        ),
        migrations.RemoveField(
            model_name='position',
            name='profiles',
        ),
        migrations.RemoveField(
            model_name='position',
            name='requested_profiles',
        ),
        migrations.AddField(
            model_name='profile',
            name='approved_positions',
            field=models.ManyToManyField(related_name='approved_profiles', to='seawatch_registration.Position'),
        ),
        migrations.AddField(
            model_name='profile',
            name='requested_positions',
            field=models.ManyToManyField(related_name='requested_profiles', to='seawatch_registration.Position'),
        ),
        migrations.DeleteModel(
            name='ProfilePosition',
        ),
    ]