from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, unique=False)
    fullName = models.CharField(
        max_length=255,   unique=True)
    phoneNumber = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    age = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='autocare/images', null=True)
    user_type = models.CharField(max_length=30)

    USERNAME_FIELD = 'phoneNumber'

    REQUIRED_FIELDS = ['fullName',
                       'email', 'age', 'avatar', 'user_type']

    def __str__(self):
        return self.username


class PartSupplier(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


class TowCarOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


class WorkShopOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


class origin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    origin = models.ForeignKey(origin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class location(models.Model):
    longlat = models.CharField(max_length=255)

    def __str__(self):
        return self.longlat


class Cars(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    carBrand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    carModel = models.CharField(max_length=255)
    carYear = models.CharField(max_length=255)
    carColor = models.CharField(max_length=255)
    plateNumber = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='autocare/images', null=True)

    def __str__(self):
        return self.carBrand.name


class Specialist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkShop(models.Model):
    workshopOwnerId = models.ForeignKey(
        WorkShopOwner, on_delete=models.CASCADE)
    origin = models.ForeignKey(
        origin, on_delete=models.CASCADE)
    locationId = models.ForeignKey(location, on_delete=models.CASCADE)
    workshopName = models.CharField(max_length=255)
    currentCars = models.IntegerField(default=1)
    contactNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='autocare/images', null=True)
    specialistName = models.ForeignKey(
        Specialist, on_delete=models.CASCADE)

    def __str__(self):
        return self.workshopName


class WorkShopImages(models.Model):
    WorkShop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    portfolio = models.ImageField(
        upload_to='autocare/workshop/images', null=True)


class CarOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(
        WorkShop, related_name='favorite', blank=True)

    def __str__(self):
        return self.user_id.username


class Request(models.Model):
    workshopId = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    carsId = models.ForeignKey(Cars, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    requestType = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, null=True)


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


class TowRequest (models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    cost = models.PositiveBigIntegerField


class workshopBrands (models.Model):
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)


class City (models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TowCar (models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    coverageCity = models.ForeignKey(City, on_delete=models.DO_NOTHING)


class product(models.Model):
    productName = models.CharField(max_length=255)

    category = models.ForeignKey(Specialist, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    productImage = models.ImageField(upload_to='autocare/images', null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.productName


class ProductPartSupplier(models.Model):
    partSupplierId = models.ForeignKey(
        User, on_delete=models.CASCADE)
    productId = models.ForeignKey(product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=4)
