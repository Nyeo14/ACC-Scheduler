# Generated by Django 3.2.5 on 2021-08-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling_application', '0014_auto_20210806_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='notif_call',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='notif_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='notif_test',
            field=models.BooleanField(default=False),
        ),
    ]
