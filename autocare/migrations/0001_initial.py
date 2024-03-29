# Generated by Django 4.2.7 on 2024-02-26 09:05

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
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand')),
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
                ('carYear', models.CharField(max_length=255)),
                ('carColor', models.CharField(max_length=255)),
                ('plateNumber', models.CharField(max_length=255, unique=True)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('carBrand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.brand')),
                ('carModel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.carmodel')),
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
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='autocare/images')),
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
            name='Origin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PartSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('storeName', models.CharField(max_length=255)),
                ('contactNumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('storeAvatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('logo', models.ImageField(null=True, upload_to='autocare/images')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('productImage', models.ImageField(null=True, upload_to='autocare/images')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestType', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(max_length=255, null=True)),
                ('carsId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.cars')),
            ],
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
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
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TowBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
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
            name='TowCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carYear', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('plateNumber', models.CharField(max_length=255, unique=True)),
                ('available', models.BooleanField(default=False)),
                ('carBrand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.towbrand')),
            ],
        ),
        migrations.CreateModel(
            name='TowOrigin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('workshopName', models.CharField(max_length=255)),
                ('currentCars', models.IntegerField(default=1)),
                ('contactNumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('logo', models.ImageField(null=True, upload_to='autocare/images')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.specialist')),
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
                ('cost', models.DecimalField(decimal_places=2, max_digits=30)),
                ('currentLocation', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
                ('towCarId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.towcars')),
            ],
        ),
        migrations.AddField(
            model_name='towcars',
            name='carOrigin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.toworigin'),
        ),
        migrations.AddField(
            model_name='towcars',
            name='coverageCity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.city'),
        ),
        migrations.AddField(
            model_name='towcars',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.towcarowner'),
        ),
        migrations.AddField(
            model_name='towbrand',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.toworigin'),
        ),
        migrations.CreateModel(
            name='storeBrands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.brand')),
                ('partSupplierId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.partsupplier')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeName', models.CharField(max_length=255)),
                ('contactNumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('avatar', models.ImageField(null=True, upload_to='autocare/images')),
                ('locationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin')),
                ('partSupplierId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.partsupplier')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='autocare.status'),
        ),
        migrations.AddField(
            model_name='request',
            name='transactionStatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='autocare.transactionstatus'),
        ),
        migrations.AddField(
            model_name='request',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autocare.carowner'),
        ),
        migrations.AddField(
            model_name='request',
            name='workshopId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autocare.workshop'),
        ),
        migrations.CreateModel(
            name='ProductPartSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('CarModel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.carmodel')),
                ('partSupplierId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.partsupplier')),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autocare.specialist'),
        ),
        migrations.CreateModel(
            name='maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts', models.DateTimeField(blank=True, null=True)),
                ('ends', models.DateTimeField(blank=True, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('description', models.CharField(max_length=255)),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
            ],
        ),
        migrations.CreateModel(
            name='checkup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts', models.DateTimeField(null=True)),
                ('ends', models.DateTimeField(null=True)),
                ('requestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.request')),
            ],
        ),
        migrations.AddField(
            model_name='cars',
            name='carOrigin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.origin'),
        ),
        migrations.AddField(
            model_name='cars',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocare.carowner'),
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
