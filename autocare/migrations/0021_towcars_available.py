# Generated by Django 4.2.7 on 2024-02-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0020_remove_towcars_avatar_remove_towcars_carcolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='towcars',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]