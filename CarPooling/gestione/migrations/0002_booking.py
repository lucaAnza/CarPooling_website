# Generated by Django 5.1 on 2024-08-09 16:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_registration_time', models.DateField(default=None)),
                ('close_registration_time', models.DateField(default=None)),
                ('max_passenger', models.IntegerField(default=0)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.car')),
                ('user_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='booking_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
