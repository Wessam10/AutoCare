# Generated by Django 4.2.7 on 2024-01-26 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0006_rename_specialistname_workshop_specialist'),
    ]

    operations = [
        migrations.CreateModel(
            name='store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeName', models.CharField(max_length=255)),
                ('contactNumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand')),
                ('locationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin')),
                ('partSupplierId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.partsupplier')),
            ],
        ),
    ]
