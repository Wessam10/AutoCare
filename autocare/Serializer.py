from rest_framework import serializers
from .models import WorkShop, workshopBrands, Specialist, Request, Brand, CarOwner, Cars,  PartSupplier, product, TowCarOwner, TowRequest, User, WorkShopOwner, origin, checkup, location, maintenance, WorkShopImages
import json


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fullName', 'username',
                  'phoneNumber', 'email', 'age',  'avatar']


class UserImageSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='avatar.url', read_only=True)

    class Meta:
        model = User
        fields = '__all__'  # ['id', 'username', 'email', 'avatar']


class CarOwnerSerializer (serializers.ModelSerializer):
    userCars = UserSerializer(source='user_Cars', read_only=True)

    class Meta:
        model = CarOwner
        fields = ['user_Cars', 'userCars']


class PartSupplierSerializer (serializers.ModelSerializer):
    class Meta:
        model = PartSupplier
        fields = ['user_id', 'productId']


class WorkShopOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id')

    class Meta:
        model = WorkShopOwner
        fields = ['user']


class BrandSerializer (serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['origin', 'name']


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
    workshopOwnerId = serializers.CharField(
        source='workshopOwnerId.user_id.username')
    # specialistName = serializers.CharField(source='Specialist.name')
    specialist = serializers.CharField(source='specialistName.name')

    class Meta:
        model = WorkShop
        fields = ['workshopOwnerId', 'brands', 'WorkShopBrands', 'originName', 'origin',  'locationId',
                  'workshopName', 'currentCars', 'contactNumber', 'specialist', 'specialistName', 'avatar']

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
    class Meta:
        model = product
        fields = ['productName', 'category',
                  'description', 'code', 'price', 'productImage']


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
    class Meta:
        car = serializers.CharField(source='Cars_model')
        model = TowCarOwner
        fields = ['user_id']
