# Generated by Django 4.2.7 on 2024-01-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0013_remove_storebrands_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='autocare/images')),
            ],
        ),
    ]
