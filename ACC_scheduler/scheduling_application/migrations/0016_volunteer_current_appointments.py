# Generated by Django 3.2.5 on 2021-08-06 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling_application', '0015_rename_language_senior_preferred_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='current_appointments',
            field=models.TextField(default='{}', editable=False),
        ),
    ]
