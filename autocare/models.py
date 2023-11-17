from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    userName = models.CharField(max_length=255, null=True)
    fullName = models.CharField(
        max_length=255,   unique=True)
    password = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    age = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(upload_to='autocare/images', null=True)

    REQUIRED_FIELDS = ['fullName', 'password',
                       'phoneNumber', 'email', 'age', 'avatar']

    def __str__(self):
        return self.username


class CarOwner(models.Model):
    userCars = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class product(models.Model):
    productName = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    productImage = models.CharField(max_length=255)


class PartSupplier(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    productId = models.ForeignKey(product, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class TowCarOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class WorkShopOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class TowRequest(models.Model):
    TowCarOwnerId = models.ForeignKey(TowCarOwner, on_delete=models.CASCADE)


class origin(models.Model):
    name = models.CharField(max_length=255)


class Brand(models.Model):
    origin = models.ForeignKey(origin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class location(models.Model):
    longlat = models.CharField(max_length=255)


class Cars(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    carBrand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    carModel = models.CharField(max_length=255)
    carYear = models.CharField(max_length=255)
    carColor = models.CharField(max_length=255)
    plateNumber = models.CharField(max_length=255)


class WorkShop(models.Model):
    workshopOwnerId = models.ForeignKey(
        WorkShopOwner, on_delete=models.CASCADE)
    origin = models.ForeignKey(
        origin, on_delete=models.CASCADE)
    brands = models.ForeignKey(
        Brand, on_delete=models.CASCADE)
    locationId = models.ForeignKey(location, on_delete=models.CASCADE)
    workshopName = models.CharField(max_length=255)
    currentCars = models.ForeignKey(Cars, on_delete=models.CASCADE)
    contactNumber = models.CharField(max_length=255)
    specialist_choices = (
        ('Car electrician', 'Car electrician'),
        ('mechanistic ', 'mechanistic'),
        ('suspension specialists', 'suspension specialists'),
    )

    specialist = models.CharField(max_length=30, choices=specialist_choices)


class Request(models.Model):
    workshopId = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    carsId = models.ForeignKey(Cars, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    date = models.DateField()


class maintenance(models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    cost = models.PositiveBigIntegerField


class checkup (models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    cost = models.PositiveBigIntegerField
