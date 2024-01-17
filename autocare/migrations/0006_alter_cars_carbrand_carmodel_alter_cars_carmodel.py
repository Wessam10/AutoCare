# Generated by Django 4.2.7 on 2024-01-17 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autocare', '0005_rename_brand_productpartsupplier_brands'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='carBrand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand'),
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand')),
            ],
        ),
        migrations.AlterField(
            model_name='cars',
            name='carModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.carmodel'),
        ),
    ]
