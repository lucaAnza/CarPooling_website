# Generated by Django 5.1 on 2024-08-28 12:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0014_car_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='close_registration_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ride',
            name='max_passenger',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ride',
            name='open_registration_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ride',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='my_rides', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ride',
            name='car',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='my_rides', to='gestione.car'),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
