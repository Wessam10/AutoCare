# Generated by Django 4.2.7 on 2024-02-26 17:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0006_alter_productpartsupplier_carmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]