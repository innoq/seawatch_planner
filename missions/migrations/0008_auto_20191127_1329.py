# Generated by Django 2.2.7 on 2019-11-27 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0007_auto_20191127_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'permissions': (('can_create_assignment', 'Create assignments'), ('can_view_assignment', 'View assignments'), ('can_update_assignment', 'Update assignments'), ('can_delete_assignment', 'Delete assignments'))},
        ),
    ]
