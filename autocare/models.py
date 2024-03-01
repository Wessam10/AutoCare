from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, unique=True)
    fullName = models.CharField(
        max_length=255,   unique=True)
    phoneNumber = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    age = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='autocare/images', null=True)
    user_type = models.CharField(max_length=30)

    USERNAME_FIELD = 'phoneNumber'

    REQUIRED_FIELDS = ['fullName',
                       'age', 'avatar', 'user_type']

    def __str__(self):
        return self.fullName


class Origin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TowOrigin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TowBrand(models.Model):
    origin = models.ForeignKey(TowOrigin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class location(models.Model):
    longlat = models.CharField(max_length=255)

    def __str__(self):
        return self.longlat


class PartSupplier(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    origin = models.ForeignKey(
        Origin, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    storeName = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    storeAvatar = models.ImageField(upload_to='autocare/images', null=True)
    logo = models.ImageField(upload_to='autocare/images', null=True)

    def __str__(self):
        return self.user_id.fullName


class TowCarOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.fullName


class WorkShopOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.fullName


class Specialist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkShop(models.Model):
    workshopOwnerId = models.ForeignKey(
        WorkShopOwner, on_delete=models.CASCADE)
    origin = models.ForeignKey(
        Origin, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    workshopName = models.CharField(max_length=255)
    currentCars = models.IntegerField(default=1)
    contactNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='autocare/images', null=True)
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to='autocare/images', null=True, blank=True)

    def __str__(self):
        return self.workshopName


class Product(models.Model):
    productName = models.CharField(max_length=255)

    category = models.ForeignKey(
        Specialist, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    productImage = models.ImageField(upload_to='autocare/images', null=True)

    def __str__(self):
        return self.productName


class Store(models.Model):
    partSupplierId = models.ForeignKey(
        PartSupplier, on_delete=models.CASCADE)

    origin = models.ForeignKey(
        Origin, on_delete=models.CASCADE)
    locationId = models.ForeignKey(location, on_delete=models.CASCADE)
    storeName = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='autocare/images', null=True)

    def __str__(self):
        return self.storeName


class CarOwner(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(
        WorkShop, related_name='favorite', blank=True)

    def __str__(self):
        return self.user_id.fullName


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Cars(models.Model):
    userId = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    carOrigin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    carBrand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    carModel = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING)
    carYear = models.CharField(max_length=255)
    carColor = models.CharField(max_length=255)
    plateNumber = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='autocare/images', null=True)

    def __str__(self):
        return self.carBrand.name


class City (models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TowCars(models.Model):
    userId = models.ForeignKey(
        TowCarOwner, on_delete=models.CASCADE)
    coverageCity = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    carOrigin = models.ForeignKey(TowOrigin, on_delete=models.CASCADE)
    carBrand = models.ForeignKey(TowBrand, on_delete=models.DO_NOTHING)
    carYear = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    plateNumber = models.CharField(max_length=255, unique=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.carBrand.name


class WorkShopImages(models.Model):
    WorkShop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    portfolio = models.ImageField(
        upload_to='autocare/workshop/images', null=True)


class TransactionStatus(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class RequestType(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Request(models.Model):
    workshopId = models.ForeignKey(
        WorkShop, on_delete=models.CASCADE, null=True)
    carsId = models.ForeignKey(Cars, on_delete=models.CASCADE)
    userId = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True)
    requestType = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    transactionStatus = models.ForeignKey(
        TransactionStatus, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.requestType


class maintenance(models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    starts = models.DateTimeField(null=True, blank=True)
    ends = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.requestId.requestType


class checkup (models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    starts = models.DateTimeField(null=True)
    ends = models.DateTimeField(null=True)
    cost = models.PositiveBigIntegerField


class TowRequest (models.Model):
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    towCarId = models.ForeignKey(TowCars, on_delete=models.CASCADE)
    cost = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    currentLocation = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    def __str__(self):
        return self.requestId.requestType


class workshopBrands (models.Model):
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)

    def __str__(self):
        return self.brands.name


class ProductPartSupplier(models.Model):
    partSupplierId = models.ForeignKey(
        PartSupplier, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    CarModel = models.ForeignKey(
        CarModel, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.productId.productName


class storeBrands (models.Model):
    partSupplierId = models.ForeignKey(
        PartSupplier, on_delete=models.CASCADE)
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.brands.name


class Images (models.Model):
    images = models.ImageField(upload_to='autocare/images', null=True)
