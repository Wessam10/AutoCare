# Generated by Django 4.2.7 on 2024-02-22 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0038_alter_request_workshopid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='towrequest',
            name='towCarLocation',
        ),
    ]