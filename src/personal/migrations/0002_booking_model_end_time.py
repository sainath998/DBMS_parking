# Generated by Django 3.2 on 2021-04-29 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_model',
            name='end_time',
            field=models.TimeField(null=True),
        ),
    ]
