# Generated by Django 2.2.9 on 2020-01-28 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0026_auto_20200127_1741'),
        ('missions', '0018_auto_20200123_1159'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='defaultassignment',
            unique_together={('position', 'ship')},
        ),
    ]