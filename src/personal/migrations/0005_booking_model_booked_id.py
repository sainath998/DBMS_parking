# Generated by Django 3.2 on 2021-04-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0004_booking_model_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_model',
            name='booked_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
