# Generated by Django 5.1 on 2024-08-13 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0007_rename_user_id_booking_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='user_id',
            new_name='user',
        ),
    ]
