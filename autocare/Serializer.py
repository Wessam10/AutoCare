from rest_framework import serializers
from .models import WorkShop, Request, Brand, CarOwner, Cars,  PartSupplier, product, TowCarOwner, TowRequest, User, WorkShopOwner, origin, checkup, location, maintenance


class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fullName', 'password',
                  'phoneNumber', 'email', 'age',  'avatar']


class UserImageSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='avatar.url', read_only=True)

    class Meta:
        model = User
        # Include other fields as needed
        fields = ('id', 'username', 'email', 'avatar')


class CarOwnerSerializer (serializers.ModelSerializer):
    car = serializers.CharField(source='user_id')

    class Meta:
        model = CarOwner
        fields = ['car']


class PartSupplierSerializer (serializers.ModelSerializer):
    class Meta:
        model = PartSupplier
        fields = ['partSupplierId', 'productId']


class WorkShopOwnerSerializer (serializers.ModelSerializer):
    model = WorkShopOwner
    fields = ['user_id']


class WorkShopSerializer (serializers.ModelSerializer):
    class Meta:
        model = WorkShop
        fields = ['__all__']


class RequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['workshopId', 'carsId', 'type', 'date']


class BrandSerializer (serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['origin', 'name']


class CarsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ['userId', 'carBrand', 'carModel',
                  'carYear', 'carColor', 'plateNumber']


class productSerializer (serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['productName', 'category',
                  'description', 'code', 'price', 'productImage']


class TowRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = TowRequest
        fields = ['TowCarOwnerId']


class OriginSerializer (serializers.ModelSerializer):
    class Meta:
        model = origin
        fields = ['name']


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
        fields = ['car',]

    # class CarSerializer(serializers.ModelSerializer):
    # user = UserCreateSerializer(source='user_id', read_only=True)
    # images = serializers.SerializerMethodField(read_only=True)
    # car_model = serializers.CharField(source='car_models', read_only=True)
    # car_brand = serializers.CharField(source='car_models.brand_id.name', read_only=True)
    # price = serializers.CharField(read_only=True)
    # province_name = serializers.CharField(source='location.province_name', read_only=True)
    # country_name = serializers.CharField(source='location.country_id.country_name', read_only=True)
    # status = serializers.SerializerMethodField(read_only=True)

    # class Meta:
    #     model = models.Car
    #     fields = [
    #         'id', 'user_id', 'user', 'mileage', 'color', 'type', 'manufacturing_year', 'clean_title', 'engine_type',
    #         'gear_type', 'cylinders', 'notes', 'price', 'location', 'province_name', 'country_name', 'car_model',
    #         'car_models', 'car_brand', 'engine_capacity', 'damage', 'drive_type', 'images', 'status']

    # def get_images(self, obj):
    #     query = models.Media.objects.filter(car_id=obj.pk).values_list('image_id__image', flat=True)

    #     data = []

    #     current_site = get_current_site(self.context['request'])
    #     for image_id__image in query:
    #         print(image_id__image)
    #         absolute_url = settings.MEDIA_URL + str(image_id__image)
    #         data.append('http://'+current_site.domain+absolute_url)

    #     return data

    # def get_status(self, obj):
    #     query = models.CarInAuction.objects.filter(car_id=obj.pk, status='sold')
    #     if query.exists():
    #         return 'sold'
    #     else:
    #         return 'for sale'
