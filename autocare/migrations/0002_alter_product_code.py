# Generated by Django 4.2.7 on 2024-02-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
