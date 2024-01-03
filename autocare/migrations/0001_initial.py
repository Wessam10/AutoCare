# Generated by Django 4.2.7 on 2024-01-03 16:15

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=255, null=True, unique=True)),
                ('fullName', models.CharField(max_length=255, unique=True)),
                ('phoneNumber', models.CharField(max_length=255, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('age', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('user_type', models.CharField(max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CarOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carModel', models.CharField(max_length=255)),
                ('carYear', models.CharField(max_length=255)),
                ('carColor', models.CharField(max_length=255)),
                ('plateNumber', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('carBrand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.brand')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.carowner')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longlat', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='origin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('productImage', models.ImageField(null=True, upload_to='autocare/images')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestType', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('notes', models.CharField(max_length=255, null=True)),
                ('carsId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.cars')),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WorkShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workshopName', models.CharField(max_length=255)),
                ('currentCars', models.IntegerField(default=1)),
                ('contactNumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('locationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin')),
                ('specialistName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.specialist')),
            ],
        ),
        migrations.CreateModel(
            name='WorkShopOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkShopImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio', models.ImageField(null=True, upload_to='autocare/workshop/images')),
                ('WorkShop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='workshopBrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.brand')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.workshop')),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='workshopOwnerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.workshopowner'),
        ),
        migrations.CreateModel(
            name='TowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
            ],
        ),
        migrations.CreateModel(
            name='TowCarOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TowCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.cars')),
                ('coverageCity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.city')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='workshopId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.workshop'),
        ),
        migrations.CreateModel(
            name='ProductPartSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand')),
                ('partSupplierId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.specialist'),
        ),
        migrations.CreateModel(
            name='PartSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField()),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
            ],
        ),
        migrations.CreateModel(
            name='checkup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField()),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
            ],
        ),
        migrations.AddField(
            model_name='carowner',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to='autocare.workshop'),
        ),
        migrations.AddField(
            model_name='carowner',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brand',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin'),
        ),
    ]
