# Generated by Django 4.2.7 on 2024-01-26 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0007_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='storeBrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.brand')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.store')),
            ],
        ),
    ]
