# Generated by Django 2.2.7 on 2019-11-27 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0008_auto_20191127_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'permissions': (('can_create_assignments', 'Create assignments'), ('can_view_assignments', 'View assignments'), ('can_update_assignments', 'Update assignments'), ('can_delete_assignments', 'Delete assignments'))},
        ),
    ]
