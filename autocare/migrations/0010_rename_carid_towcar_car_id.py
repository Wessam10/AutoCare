# Generated by Django 4.2.7 on 2023-12-26 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0009_remove_towcar_blatenumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='towcar',
            old_name='carId',
            new_name='car_id',
        ),
    ]