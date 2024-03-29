from rest_framework import serializers
from .models import WorkShop, CarModel, workshopBrands, Images, RequestType, TowCars, City, TransactionStatus, Status, Specialist, TowBrand, Store, storeBrands, TowOrigin, ProductPartSupplier, Request, Specialist, Brand, CarOwner, Cars,  PartSupplier, Product, TowCarOwner, TowRequest, User, WorkShopOwner, Origin, checkup, location, maintenance, WorkShopImages
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import hashlib


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        # IF SOMTHING GOES WRONG
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
    originName = originName = serializers.CharField(
        source='origin.name', read_only=True)

    class Meta:
        model = TowBrand
        fields = ['origin',  'originName', 'id', 'name']


class PartSupplierSerializer (serializers.ModelSerializer):
    brands = serializers.ListField(write_only=True)
    storeBrand = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(
        source='origin.name', read_only=True)
    user = UserSerializer(source='user_id', read_only=True)
    # storeLogo = serializers.ImageField(source='logo')
    # avatarStore = serializers.ImageField(source='storeAvatar')

    class Meta:
        model = PartSupplier
        fields = ['id', 'user_id', 'user', 'brands', 'storeBrand', 'originName', 'origin',  'location', 'address',
                  'storeName', 'contactNumber', 'logo', 'storeAvatar']

    def create(self, validated_data):
        brands_data = validated_data.pop(
            'brands', [])  # Extract brands data

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


class ProductPartSupplierSerializer(serializers.ModelSerializer):
    # brands = serializers.ListField(write_only=True)
    partBrandsName = serializers.SerializerMethodField(read_only=True)
    # carModel = serializers.SerializerMethodField(read_only=True)
    productName = serializers.CharField(
        source='productId.productName', read_only=True)
    category = serializers.CharField(
        source='productId.category', read_only=True)
    description = serializers.CharField(
        source='productId.description', read_only=True)
    productImage = serializers.ImageField(
        source='productId.productImage', read_only=True)
    # productId = serializers.ListField(write_only=True)

    class Meta:
        model = ProductPartSupplier
        fields = ['partSupplierId',
                  'productId', 'productName', 'category', 'CarModel', 'description', 'status', 'productImage',
                  'partBrandsName']

    def create(self, validated_data):
        return super().create(validated_data)

    def get_partBrandsName(self, obj):
        brand_id = obj.CarModel.brand.pk
        brand_name = Brand.objects.filter(id=brand_id)
        return brand_name.values()

    # def get_carModel(self, obj):
    #     brand_id = obj.brands_id
    #     Brand = CarModel.objects.filter(partSupplierId=obj.pk)
    #     return Brand.values_list("brands__name", flat=True)


class WPartSupplierSerializer(serializers.ModelSerializer):
    storeLogo = serializers.SerializerMethodField()
    AvatarStore = serializers.SerializerMethodField()

    def get_avatarLogo(self, obj):
        if obj['logo']:
            return self.context['request'].build_absolute_uri(obj['logo'])
        return None

    def get_storeLogo(self, obj):
        print(obj)
        print(obj.pk)
        Brand = PartSupplier.objects.filter(partSupplierId=obj.pk)
        return ProductPartSupplier.values_list("productId.productImage", flat=True)

    class Meta:
        model = ProductPartSupplier
        fields = ['partSupplierId', 'avatarLogo', 'AvatarStore']


class WorkShopOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = WorkShopOwner
        fields = ['id', 'user_id', 'user']


class TowCarOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = TowCarOwner
        fields = ['user_id', 'user']


class workshopBrandsSerializer (serializers.ModelSerializer):
    class Meta:
        model = workshopBrands
        fields = ['brands', 'workshop']


class storeBrandsSerializer (serializers.ModelSerializer):
    name = serializers.CharField(source='brands.name', read_only=True)

    class Meta:
        model = storeBrands
        fields = ['brands', 'name', 'partSupplierId']


class OriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ['id', 'name']


class TowOriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowOrigin
        fields = ['id', 'name']


class SpecialistSerializer (serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['name']


class WorkShopSerializer (serializers.ModelSerializer):
    ownerInfo = WorkShopOwnerSerializer(
        source='workshopOwnerId', read_only=True)
    brands = serializers.ListField(write_only=True)
    WorkShopBrands = serializers.SerializerMethodField(read_only=True)
    originName = serializers.CharField(source='origin.name', read_only=True)
    specialistName = serializers.CharField(
        source='specialist.name', read_only=True)
    # workshopOwnerId = serializers.CharField(
    #     source='workshopOwnerId.user_id.username')

    class Meta:
        model = WorkShop
        fields = ['id', 'workshopOwnerId', 'ownerInfo', 'brands', 'WorkShopBrands', 'originName', 'origin',  'location', 'address',
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


class CarsSerializer (serializers.ModelSerializer):
    carId = serializers.CharField(
        source='id', read_only=True)
    name = serializers.CharField(
        source='userId.user_id.fullName', read_only=True)
    brandName = serializers.CharField(
        source='carBrand.name', read_only=True)
    originName = serializers.CharField(
        source='carOrigin.name', read_only=True)
    modelName = serializers.CharField(
        source='carModel.name', read_only=True)

    class Meta:
        model = Cars
        fields = ['carId', 'userId', 'name', 'carBrand', 'brandName', 'carModel', 'modelName', 'carOrigin', 'originName',
                  'carYear', 'carColor', 'plateNumber', 'avatar']


class maintenanceSerializer (serializers.ModelSerializer):
    # infoRequest = RequestSerializer(source='requestId', read_only=True)
    # Explicitly define the field type if needed
    starts = serializers.DateTimeField(required=False)
    ends = serializers.DateTimeField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = maintenance
        fields = ['requestId', 'starts',
                  'ends', 'cost', 'description']


class RequestSerializer (serializers.ModelSerializer):
    car = CarsSerializer(source='carsId', read_only=True)
    workshopName = serializers.CharField(
        source='workshopId.workshopName', read_only=True)
    statusName = serializers.CharField(
        source='status.name', read_only=True)
    transactionStatusName = serializers.CharField(
        source='transactionStatus.name', read_only=True)
    startTime = serializers.SerializerMethodField(read_only=True)
    endTime = serializers.SerializerMethodField(read_only=True)
    cost = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'workshopId', 'workshopName', 'carsId', 'car',
                  'userId', 'requestType', 'startTime', 'endTime', 'cost', 'description', 'notes', 'date', 'status', 'statusName', 'transactionStatus', 'transactionStatusName']

    def get_startTime(self, obj):
        Brand = maintenance.objects.filter(requestId=obj.pk)
        starts_list = Brand.values_list("starts", flat=True)
        starts_str = ", ".join(str(start) for start in starts_list)
        return starts_str

    def get_cost(self, obj):
        Brand = maintenance.objects.filter(requestId=obj.pk)
        cost_list = Brand.values_list("cost", flat=True)
        cost_str = ", ".join(str(c) for c in cost_list)
        return cost_str

    def get_endTime(self, obj):
        Brand = maintenance.objects.filter(requestId=obj.pk)
        ends_list = Brand.values_list("ends", flat=True)
        ends_str = ", ".join(str(end) for end in ends_list)
        return ends_str

    def get_description(self, obj):
        Brand = maintenance.objects.filter(requestId=obj.pk)
        desc_list = Brand.values_list("description", flat=True)
        desc_str = ", ".join(str(desc) for desc in desc_list)
        return desc_str


class TowCarsSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowCars
        fields = ['userId', 'carBrand', 'location', 'carOrigin', 'coverageCity',
                  'carYear', 'plateNumber', 'available']


class productSerializer (serializers.ModelSerializer):
    productCode = serializers.CharField(source='code', read_only=True)
    categoryName = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'productName', 'category', 'categoryName',
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
    request = RequestSerializer(source='requestId', read_only=True)

    class Meta:
        model = TowRequest
        fields = ['towCarId', 'request', 'requestId', 'cost',
                  'currentLocation', 'destination']


class checkupSerializer (serializers.ModelSerializer):
    class Meta:
        model = checkup
        fields = ['requestId', 'starts', 'ends', 'cost']


class locationSerializer (serializers.ModelSerializer):
    class Meta:
        model = location
        fields = ['longlat']


class TowCarOwnerSerializer (serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
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


class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionStatus
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestType
        fields = ['id', 'name']
