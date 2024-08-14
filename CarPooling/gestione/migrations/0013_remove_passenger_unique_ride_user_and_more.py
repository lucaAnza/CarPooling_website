# Generated by Django 5.1 on 2024-08-14 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0012_booking_booking_primary_key'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='passenger',
            name='unique_ride_user',
        ),
        migrations.AddConstraint(
            model_name='passenger',
            constraint=models.UniqueConstraint(fields=('ride', 'user'), name='passenger_primary_key'),
        ),
        migrations.AddConstraint(
            model_name='ride',
            constraint=models.UniqueConstraint(fields=('id', 'car'), name='ride_primary_key'),
        ),
    ]
