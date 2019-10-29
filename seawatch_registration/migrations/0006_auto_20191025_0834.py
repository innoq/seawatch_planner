# Generated by Django 2.2.6 on 2019-10-25 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seawatch_registration', '0005_auto_20191025_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seawatch_registration.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('mandatory', models.BooleanField()),
                ('profiles', models.ManyToManyField(through='seawatch_registration.Answer', to='seawatch_registration.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seawatch_registration.Question'),
        ),
    ]