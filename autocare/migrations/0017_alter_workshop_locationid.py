# Generated by Django 4.2.7 on 2024-02-09 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0016_remove_partsupplier_locationid_partsupplier_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='locationId',
            field=models.CharField(max_length=255),
        ),
    ]