# Generated by Django 4.2.7 on 2024-01-03 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
