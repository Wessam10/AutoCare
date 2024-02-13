from rest_framework import serializers
from .models import WorkShop, CarModel, workshopBrands, Images, TowCars, City, Specialist, TowBrand, Store, storeBrands, TowOrigin, ProductPartSupplier, Request, Specialist, Brand, CarOwner, Cars,  PartSupplier, Product, TowCarOwner, TowRequest, User, WorkShopOwner, origin, checkup, location, maintenance, WorkShopImages
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import hashlib


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'fullName',
                  'phoneNumber', 'email', 'avatar', 'password', 'user_type']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        return token


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


class BrandSerializer (serializers.ModelSerializer):
    originName = serializers.CharField(source='origin.name', read_only=True)

    class Meta:
        model = Brand
        fields = ['origin',  'originName', 'id', 'name']


class TowBrandSerializer (serializers.ModelSerializer):
    originName = serializers.CharField(source='origin.name', read_only=True)

    class Meta:
        model = TowBrand
        fields = ['origin',  'originName', 'id', 'name']


class ProductPartSupplierSerializer(serializers.ModelSerializer):
    # brands = serializers.ListField(write_only=True)
    partBrands = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductPartSupplier
        fields = ['partSupplierId',
                  'productId', 'brands', 'count', 'partBrands', 'price']

    # def create(self, validated_data):
    #     brands_data = validated_data.pop('brands', [])  # Extract brands data

    #     workshop = PartSupplier.objects.create(**validated_data)
    #     print('brands_data', brands_data)
    #     print(type(brands_data))
    #     print("aaaa1234")
    #     for brand_string in brands_data[0].split(','):
    #         shopBrands = storeBrandsSerializer(
    #             data={'partSupplierId': workshop.pk, 'brands': brand_string})
    #         shopBrands.is_valid(raise_exception=True)
    #         shopBrands.save()

    #     return workshop

    def get_partBrands(self, obj):
        print(obj)
        print(obj.pk)
        Brand = storeBrands.objects.filter(partSupplierId=obj.pk)
        return Brand.values_list("brands__name", flat=True)


class PartSupplierSerializer (serializers.ModelSerializer):
    brands = serializers.ListField(write_only=True)
    storeBrand = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(source='origin.name', read_only=True)
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = PartSupplier
        fields = ['user_id', 'user', 'brands', 'storeBrand', 'originName', 'origin',  'location', 'address',
                  'storeName', 'contactNumber', 'logo', 'avatar']

    def create(self, validated_data):
        brands_data = validated_data.pop('brands', [])  # Extract brands data

        workshop = PartSupplier.objects.create(**validated_data)
        print('brands_data', brands_data)
        print(type(brands_data))
        for brand_string in brands_data[0].split(','):
            shopBrands = storeBrandsSerializer(
                data={'partSupplierId': workshop.pk, 'brands': brand_string})
            shopBrands.is_valid(raise_exception=True)
            shopBrands.save()

        return workshop

    def get_storeBrand(self, obj):
        print(obj)
        print(obj.pk)
        Brand = storeBrands.objects.filter(partSupplierId=obj.pk)
        return Brand.values_list("brands__name", flat=True)


class WorkShopOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = WorkShopOwner
        fields = ['id', 'user_id', 'user']

    def create(self, validated_data):
        return super().create(validated_data)


class workshopBrandsSerializer (serializers.ModelSerializer):
    class Meta:
        model = workshopBrands
        fields = ['brands', 'workshop']


class storeBrandsSerializer (serializers.ModelSerializer):
    class Meta:
        model = storeBrands
        fields = ['brands', 'partSupplierId']


class OriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = origin
        fields = ['id', 'name']


class TowOriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowOrigin
        fields = ['name']


class SpecialistSerializer (serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['name']


class WorkShopSerializer (serializers.ModelSerializer):
    brands = serializers.ListField(write_only=True)
    WorkShopBrands = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(source='origin.name', read_only=True)
    specialistName = serializers.CharField(
        source='specialist.name', read_only=True)
    # workshopOwnerId = serializers.CharField(
    #     source='workshopOwnerId.user_id.username')

    class Meta:
        model = WorkShop
        fields = ['workshopOwnerId', 'brands', 'WorkShopBrands', 'originName', 'origin',  'location', 'address',
                  'workshopName', 'currentCars', 'contactNumber',  'specialist', 'specialistName', 'avatar', 'logo']

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


class StoreSerializer (serializers.ModelSerializer):
    brands = serializers.ListField(write_only=True)
    storeBrand = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(source='origin.name', read_only=True)

    # workshopOwnerId = serializers.CharField(
    #     source='workshopOwnerId.user_id.username')

    class Meta:
        model = Store
        fields = ['partSupplierId', 'brands', 'storeBrand', 'originName', 'origin',  'locationId', 'address',
                  'storeName', 'contactNumber', 'avatar']

    def create(self, validated_data):
        brands_data = validated_data.pop('brands', [])  # Extract brands data

        workshop = Store.objects.create(**validated_data)
        print('brands_data', brands_data)
        print(type(brands_data))
        for brand_string in brands_data[0].split(','):
            print(brand_string)
            shopBrands = storeBrandsSerializer(
                data={'store': workshop.pk, 'brands': brand_string})
            shopBrands.is_valid(raise_exception=True)
            shopBrands.save()

        return workshop

    def get_storeBrand(self, obj):
        print(obj)
        print(obj.pk)
        Brand = storeBrands.objects.filter(store_id=obj.pk)
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
        fields = ['userId', 'carBrand', 'carModel', 'carOrigin',
                  'carYear', 'carColor', 'plateNumber', 'avatar']


class TowCarsSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowCars
        fields = ['userId', 'carBrand', 'carOrigin', 'coverageCity',
                  'carYear', 'plateNumber']


class productSerializer (serializers.ModelSerializer):
    productCode = serializers.CharField(source='code', read_only=True)

    class Meta:
        model = Product
        fields = ['productName', 'category',
                  'description', 'productCode', 'productImage']

    def create(self, validated_data):
        Id = Product.objects.all().last().pk
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


# class TowCarSerializer(serializers.ModelSerializer):
#     carId = TowCarsSerializer(source='car_id', read_only=True)

#     class Meta:
#         model = TowCar
#         fields = ['userId', 'car_id', 'carId', 'coverageCity']


class specialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['id', 'name']


class CarModelSerializer(serializers.ModelSerializer):
    brandName = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = CarModel
        fields = ['brand', 'brandName', 'id', 'name']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'images']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']
