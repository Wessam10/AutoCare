from rest_framework import serializers
from .models import WorkShop, workshopBrands, TowCar, Specialist, ProductPartSupplier, Request, Specialist, Brand, CarOwner, Cars,  PartSupplier, product, TowCarOwner, TowRequest, User, WorkShopOwner, origin, checkup, location, maintenance, WorkShopImages
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import hashlib


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fullName',
                  'phoneNumber', 'email', 'avatar', 'password', 'user_type']


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['user_type'] = user.user_type


class UserImageSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='avatar.url', read_only=True)

    class Meta:
        model = User
        fields = '__all__'  # ['id', 'username', 'email', 'avatar']


class CarOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = CarOwner
        fields = ['user_id', 'user']


class PartSupplierSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = PartSupplier
        fields = ['user_id', 'user']


class WorkShopOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = WorkShopOwner
        fields = ['user_id', 'user']


class BrandSerializer (serializers.ModelSerializer):
    originName = serializers.CharField(source='origin.name', read_only=True)

    class Meta:
        model = Brand
        fields = ['origin',  'originName', 'id', 'name']


class workshopBrandsSerializer (serializers.ModelSerializer):
    class Meta:
        model = workshopBrands
        fields = ['brands', 'workshop']


class OriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = origin
        fields = ['name']


class SpecialistSerializer (serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['name']


class WorkShopSerializer (serializers.ModelSerializer):
    brands = serializers.ListField(write_only=True)
    WorkShopBrands = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(source='origin.name', read_only=True)
    # workshopOwnerId = serializers.CharField(
    #     source='workshopOwnerId.user_id.username')

    class Meta:
        model = WorkShop
        fields = ['workshopOwnerId', 'brands', 'WorkShopBrands', 'originName', 'origin',  'locationId', 'address',
                  'workshopName', 'currentCars', 'contactNumber',   'specialistName', 'avatar']

    def create(self, validated_data):
        brands_data = validated_data.pop('brands', [])  # Extract brands data

        workshop = WorkShop.objects.create(**validated_data)
        print('brands_data', brands_data)
        print(type(brands_data))
        for brand_string in brands_data[0].split(','):
            print(brand_string)
            shopBrands = workshopBrandsSerializer(
                data={'workshop': workshop.pk, 'brands': brand_string})
            shopBrands.is_valid(raise_exception=True)
            shopBrands.save()

        return workshop

    def get_WorkShopBrands(self, obj):
        print(obj)
        print(obj.pk)
        Brand = workshopBrands.objects.filter(workshop_id=obj.pk)
        return Brand.values_list("brands__name", flat=True)


class WorkShopImageSerializer (serializers.ModelSerializer):
    WorkShopInfo = WorkShopSerializer(source='WorkShop', read_only=True)
    # def create(self, validated_data):
    #     WorkShop_id = self.context['WorkShop_id']
    #     return WorkShopImages.objects.create(WorkShop_id=WorkShop_id, **validated_data)

    class Meta:
        model = WorkShopImages
        fields = ['portfolio', 'WorkShop', 'WorkShopInfo']


class RequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['workshopId', 'carsId',
                  'userId', 'category', 'date', 'status']


class CarsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ['userId', 'carBrand', 'carModel',
                  'carYear', 'carColor', 'plateNumber', 'avatar']


class productSerializer (serializers.ModelSerializer):
    productCode = serializers.CharField(source='code', read_only=True)

    class Meta:
        model = product
        fields = ['productName', 'category',
                  'description', 'productCode', 'productImage']

    def create(self, validated_data):
        Id = product.objects.all().last().pk
        name = validated_data.get(
            'productName', [])  # Extract brands data
        print(Id)
        data = str(Id+1) + name
        print(data)

        # Hash the data using MD5
        hashed_data = hashlib.shake_128(data.encode()).hexdigest(2)
        print(hashed_data)

        # Truncate the hashed data to 5 characters

        print(hashed_data)
        validated_data['code'] = hashed_data

        return super().create(validated_data)
        # def create(self, validated_data):
    #     print(validated_data)
    #     name = validated_data.get(
    #         'productName', [])  # Extract brands data
    #     Id = validated_data.get(
    #         'id', [])  # Extract brands data
    #     print('aaaa')

    #     data = name + str(Id)

    #     # Hash the data using MD5
    #     hashed_data = hashlib.md5(data.encode()).hexdigest()

    #     # Truncate the hashed data to 5 characters
    #     truncated_data = hashed_data[:5]
    #     product = productSerializer(
    #         data={'productCode': truncated_data})
    #     product.is_valid(raise_exception=True)
    #     product.save()

    #     return


class TowRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowRequest
        fields = ['TowCarOwnerId']


class checkupSerializer (serializers.ModelSerializer):
    class Meta:
        model = checkup
        fields = ['requestId', 'starts', 'ends', 'cost']


class locationSerializer (serializers.ModelSerializer):
    class Meta:
        model = location
        fields = ['longlat']


class maintenanceSerializer (serializers.ModelSerializer):
    class Meta:
        model = maintenance
        fields = ['requestId', 'starts', 'ends', 'cost']


class TowCarOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        car = serializers.CharField(source='Cars_model')
        model = TowCarOwner
        fields = ['user_id', 'user']


class TowCarSerializer(serializers.ModelSerializer):
    carId = CarsSerializer(source='car_id', read_only=True)

    class Meta:
        model = TowCar
        fields = ['userId', 'car_id', 'carId', 'coverageCity']


class specialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['id', 'name']


class ProductPartSupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPartSupplier
        fields = ['partSupplierId',
                  'productId', 'brand', 'count', 'price']
