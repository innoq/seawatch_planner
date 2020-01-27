# Generated by Django 2.2.7 on 2020-01-23 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_auto_20191118_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seawatch_registration.Profile', verbose_name='Profile'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], max_length=10, verbose_name='Status'),
        ),
    ]
