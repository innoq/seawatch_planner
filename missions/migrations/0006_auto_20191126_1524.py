# Generated by Django 2.2.7 on 2019-11-26 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0005_auto_20191126_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ship',
            options={'permissions': (('can_create_ships', 'Create ships'), ('can_view_ships', 'View ships'), ('can_update_ships', 'Update ships'), ('can_delete_ships', 'Delete ships'))},
        ),
    ]
