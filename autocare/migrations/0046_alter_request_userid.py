# Generated by Django 4.2.7 on 2024-02-23 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0045_rename_partsupplier_id_productpartsupplier_partsupplierid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autocare.carowner'),
        ),
    ]
