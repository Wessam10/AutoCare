from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView


from . import models
from .models import (Brand, CarOwner, Cars, PartSupplier, Request, Specialist,
                     TowCarOwner, TowRequest, User, WorkShop, WorkShopImages, workshopBrands,
                     WorkShopOwner, checkup, location, maintenance, origin, City, ProductPartSupplier,
                     Product, TowCars, CarModel, TowBrand, TowOrigin, storeBrands, Images, Store)
from .permission import CarOwnerAuth, workshopOwnerAuth, PartSupplierAuth, TowCarOwnerAuth
from .Serializer import (BrandSerializer, CarOwnerSerializer, CarsSerializer, TowBrandSerializer, TowOriginSerializer,
                         OriginSerializer, PartSupplierSerializer,
                         RequestSerializer, TowCarOwnerSerializer,
                         TowRequestSerializer, UserImageSerializer,
                         UserSerializer, WorkShopImageSerializer,
                         WorkShopOwnerSerializer, WorkShopSerializer,
                         checkupSerializer, locationSerializer,
                         maintenanceSerializer, productSerializer, ImagesSerializer, CitySerializer, TowCarsSerializer, StoreSerializer, storeBrandsSerializer, CarModelSerializer, specialistSerializer, ProductPartSupplierSerializer, MyTokenObtainPairSerializer)
# C:\Users\MAVERICK\Documents\HRMS\AutoCareCar


def responseData(data: dict, status: bool, message: str):
    response = {'data': data, 'status': status, 'message': message}
    return response


class MyTokenObtainPairView(TokenObtainPairView):
    # serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("aaaaaaaaaaa11111aaaaaaaaaaa")
        if serializer.is_valid():
            user = serializer.user
            print('b')
            tokens = serializer.validated_data
            print('Serializer is_valid:', serializer.is_valid())

            response_data = {
                'data': {
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                    'user_type': user.user_type
                },
                'status': True,
                'message': 'Login successful.'
            }
            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            'status': 'error',
            'message': 'Invalid credentials.',
            'status': False,
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     if hasattr(user, 'PartSupplier'):
    #         print('token')
    #         token['usertype'] = User.PartSupplier.user_type
    #     elif hasattr(user, 'TowCarOwner'):
    #         token['usertype'] = User.TowCarOwner.user_type
    #     elif hasattr(user, 'WorkShopOwner'):
    #         token['usertype'] = User.WorkShopOwner.user_type
    #     elif hasattr(user, 'CarOwner'):
    #         token['usertype'] = User.CarOwner.user_type

    #     return token


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class WorkShopViewSet (ModelViewSet):
    queryset = WorkShop.objects.all().order_by('pk')
    serializer_class = WorkShopSerializer
    # permission_classes = [IsAuthenticated, workshopOwnerAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin', 'specialist']

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_name = self.request.query_params.get('brands')
        print(brand_name)

        if brand_name:
            queryset = WorkShop.objects.filter(workshopbrands=brand_name)
            print(queryset)
            if not queryset.exists():
                raise NotFound("Workshops not found for specified brand.")
        return queryset

    # def get_queryset(self):
    #     user_id = self.request.user.pk
    #     try:
    #         car_owner = CarOwner.objects.get(user_id=user_id)
    #         return Cars.objects.filter(userId=car_owner.pk).order_by('pk')
    #     except CarOwner.DoesNotExist:
    #         raise NotFound("Car owner not found.")

    def create(self, request, *args, **kwargs):
        print('wwww')
        # TODO BTING ID FORM REQUEST AND ADD IT TO DATA
        request.data._mutable = True
        user = self.request.user.pk
        print(request.data)
        ShopOwner = WorkShopOwner.objects.get(user_id=user)
        print(ShopOwner)
        request.data["workshopOwnerId"] = ShopOwner.pk
        print('1')
        return super().create(request, *args, **kwargs)


class RequestViewSet (ModelViewSet):
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['carId']


class BrandViewSet (ModelViewSet):
    queryset = Brand.objects.all().order_by('pk')
    serializer_class = BrandSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin']


class TowBrandViewSet (ModelViewSet):
    queryset = TowBrand.objects.all().order_by('pk')
    serializer_class = TowBrandSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin']


class CarOwnerViewSet (ModelViewSet):
    queryset = CarOwner.objects.all().order_by('pk')
    serializer_class = CarOwnerSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_field = ['userId']

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        print(request.data)
        request_data = request.data
        password = request.data.get('password')

        # Hash the password
        hashed_password = make_password(password)

        # Update the request data with the hashed password
        request.data['password'] = hashed_password
        userInfo = {}
        userInfo["user_type"] = "Car Owner"
        for user_data in request_data:
            print(user_data)
            userInfo[user_data] = request_data.get(user_data, None)

        user = UserSerializer(data=userInfo)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        print('aaaa')
        print(user_instance.pk)
        request.data["user_id"] = user_instance.pk
        return super().create(request, *args, **kwargs)
    # permission_classes = [IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     queryset = User.objects.all()
    #     serializer = CarOwnerSerializer(queryset)
    #     user = request.user_id
    #     userCars = User.objects.filter(id=user)
    #     if userCars.exists:
    #         serializers = CarOwnerSerializer(data=userCars)
    #         print(serializers.data)
    #         return Response(responseData(data=serializer.data, message='User info', status=True), status=status.HTTP_200_OK)
    #     else:
    #         return Response(responseData(data=None, message='Invalid data', status=False), status=status.HTTP_200_OK)


class CarsViewSet (ModelViewSet):
    queryset = Cars.objects.all().order_by('pk')
    serializer_class = CarsSerializer
    # permission_classes = [IsAuthenticated, CarOwnerAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['userId ']

    def get_queryset(self):
        user_id = self.request.user.pk
        try:
            car_owner = CarOwner.objects.get(user_id=user_id)
            return Cars.objects.filter(userId=car_owner.pk).order_by('pk')
        except CarOwner.DoesNotExist:
            raise NotFound("Car owner not found.")

    def create(self, request, *args, **kwargs):
        print('aaaa')
        request.data._mutable = True
        user = self.request.user.pk
        carOwner = CarOwner.objects.get(user_id=user)
        print(user)
        request.data["userId"] = carOwner.pk
        print('aaaa')

        return super().create(request, *args, **kwargs)


class PartSupplierViewSet (ModelViewSet):
    queryset = PartSupplier.objects.all().order_by('pk')
    serializer_class = PartSupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin__brand']
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        print(request.data)
        request_data = request.data
        password = request.data.get('password')

        # Hash the password
        hashed_password = make_password(password)

        # Update the request data with the hashed password
        request.data['password'] = hashed_password
        userInfo = {}
        userInfo["user_type"] = "Parts Supplier"
        for user_data in request_data:
            print(user_data)
            userInfo[user_data] = request_data.get(user_data, None)
        user = UserSerializer(data=userInfo)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        print('aaaa')
        print(user_instance.pk)
        request.data["user_id"] = user_instance.pk
        us = User.objects.get(id=user_instance.pk)
        token_serializer = MyTokenObtainPairSerializer()
        token = token_serializer.get_token(us)
        k = self.get_serializer(data=request_data)
        k.is_valid()
        k.save()
        # Include the token in the response data
        response_data = {
            'token': str(token.access_token),

            'user': user_instance.pk
        }

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)


class productViewSet (ModelViewSet):
    queryset = Product.objects.all().order_by('pk')
    serializer_class = productSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        user = request.user.pk
        partOwner = CarOwner.objects.get(user_id=user)
        request.data['user_id'] = partOwner
        print('abv')
        return super().create(request, *args, **kwargs)


class TowCarOwnerViewSet (ModelViewSet):
    queryset = TowCarOwner.objects.all().order_by('pk')
    serializer_class = TowCarOwnerSerializer
    # permission_classes = [IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs):
    #     user = request.user_id
    #     serializer = TowCarOwnerSerializer
    #     car = User.objects.filter(id=user)
    #     if car.exists:
    #         serializers = TowCarOwnerSerializer(data=car)
    #         print(serializers.data)
    #         return Response(responseData(data=serializer.data, message='User info', status=True), status=status.HTTP_200_OK)
    #     else:
    #         return Response(responseData(data=None, message='Invalid data', status=False), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request_data = request.data
        password = request.data.get('password')

        # Hash the password
        hashed_password = make_password(password)

        # Update the request data with the hashed password
        request.data['password'] = hashed_password
        user_info = {}
        user_info["user_type"] = "Tow Car Owner"
        for user_data in request_data:
            print(user_data)
            user_info[user_data] = request_data.get(user_data, None)

        user = UserSerializer(data=user_info)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        request_data["user_id"] = workshopUser.pk
        us = User.objects.get(id=workshopUser.pk)
        token_serializer = MyTokenObtainPairSerializer()
        token = token_serializer.get_token(us)
        print(MyTokenObtainPairSerializer)
        print(us)
        print(token)
        # Include the token in the response data
        response_data = {
            'access': str(token.access_token),
            'refresh': str(token),

            'user': workshopUser.pk
        }
        k = self.get_serializer(data=request_data,)
        k.is_valid()
        k.save()
        print(k)

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)
        print('aaaa')
        # return super().create(request, *args, **kwargs)


class TowRequestViewSet (ModelViewSet):
    queryset = TowRequest.objects.all().order_by('pk')
    serializer_class = TowRequestSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet (ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


class WorkShopOwnerViewSet (ModelViewSet):
    queryset = WorkShopOwner.objects.all().order_by('pk')
    serializer_class = WorkShopOwnerSerializer

    def list(self, request, *args, **kwargs):
        print('user')
        user = request.user.pk
        work = WorkShop.objects.filter(workshopOwnerId__user_id=user)
        seri = WorkShopSerializer(work, many=True)
        print('www')
        return Response(responseData(data=seri.data, message='Invalid data', status=False), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request_data = request.data
        password = request.data.get('password')

        # Hash the password
        hashed_password = make_password(password)

        # Update the request data with the hashed password
        request.data['password'] = hashed_password
        user_info = {}
        user_info["user_type"] = "Workshop Owner"
        for user_data in request_data:
            print(user_data)
            user_info[user_data] = request_data.get(user_data, None)

        user = UserSerializer(data=user_info)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        workshopUser
        print(workshopUser)
        request_data["user_id"] = workshopUser.pk
        print('done')
        us = User.objects.get(id=workshopUser.pk)
        token_serializer = MyTokenObtainPairSerializer()
        token = token_serializer.get_token(us)
        print(MyTokenObtainPairSerializer)
        print(us)
        print(token)
        # Include the token in the response data
        response_data = {
            'token': str(token.access_token),

            'user': workshopUser.pk
        }
        k = self.get_serializer(data=request_data,)
        k.is_valid()
        k.save()
        print(k)

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        serialized = WorkShopOwnerSerializer(
            request.user, data=request.data, partial=True)
        return Response(status=status.HTTP_202_ACCEPTED)


class OriginViewSet (ModelViewSet):
    queryset = origin.objects.all().order_by('pk')
    serializer_class = OriginSerializer


class TowOriginViewSet (ModelViewSet):
    queryset = TowOrigin.objects.all().order_by('pk')
    serializer_class = TowOriginSerializer


class CheckupViewSet (ModelViewSet):
    queryset = checkup.objects.all().order_by('pk')
    serializer_class = checkupSerializer
    permission_classes = [IsAuthenticated]


class locViewSet (ModelViewSet):
    queryset = location.objects.all()
    serializer_class = locationSerializer


class MaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer
    permission_classes = [IsAuthenticated]


class userImagesViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Get the user object using DRF's built-in method
        user = self.queryset.get(pk=self.request.user.pk)
        print(user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkShopImagesViewSet (ModelViewSet):
    queryset = WorkShopImages.objects.all()
    serializer_class = WorkShopImageSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        user_id = self.request.user.pk
        print(user_id)
        workshops = WorkShop.objects.get(workshopOwnerId__user_id=user_id)
        workshop_id = workshops.pk
        print(workshop_id)
        request.data['WorkShop'] = workshop_id
        print(dict(request.data))
        # print(request.data['WorkShop'])
        return super().create(request, *args, **kwargs)


class TowCarViewSet(ModelViewSet):
    queryset = TowCars.objects.filter()
    serializer_class = TowCarsSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request_data = request.data
        user = self.request.user.pk
        print('before')
        carOwner = TowCarOwner.objects.get(user_id=user)
        print('after')
        request.data["userId"] = carOwner.pk

        towCar_info = {}
        for user_data in request_data:
            print(user_data)
            towCar_info[user_data] = request_data.get(user_data, None)
        car = TowCarsSerializer(data=towCar_info)
        car.is_valid(raise_exception=True)
        print(TowCarsSerializer)
        print("1!!!!")
        workshopUser = car.save()
        print(workshopUser.pk)

        return Response(status=status.HTTP_200_OK)


class ToggleTowCarAvailability(generics.UpdateAPIView):
    queryset = TowCars.objects.all()
    serializer_class = TowCarsSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.available = not instance.available
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SpecialistViewSet (ModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = specialistSerializer


class Origin_BrandViewSet (ModelViewSet):
    queryset = Brand.objects.filter()
    serializer_class = BrandSerializer

    def list(self, request, *args, **kwargs):
        data = {}
        serializer = self.get_serializer(self.queryset, many=True)
        origins = origin.objects.all()
        for ori in origins:
            origin_name = ori
            brand_list = Brand.objects.filter(origin=ori)
            if origin_name in data:
                data[origin_name].append(brand_list)
            else:
                data[origin_name] = [brand_list]

        return super().list(request, *args, **kwargs)


class favoriteViewSet (ModelViewSet):
    queryset = CarOwner.objects.filter()
    serializer_class = CarOwnerSerializer

    def post(request, product_id):

        WorkShop = get_object_or_404(WorkShop, pk=id)
        if WorkShop.favorite.filter(id=request.user.id).exist():
            Product.favorite.remove(request.user)
        else:
            Product.favorite.add(request.user)

    def retrieve(self, request, *args, **kwargs):
        user = request.user_id
        favorite = WorkShop.favorite.all()
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductPartViewSet (ModelViewSet):
    queryset = ProductPartSupplier.objects.filter()
    serializer_class = ProductPartSupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partSupplierId']

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data
        user = self.request.user.pk
        part_supplier = PartSupplier.objects.get(user_id=user)
        request.data['partSupplierId'] = part_supplier.pk
        print("1")
        print(part_supplier.pk)

        product_info = {}
        for product_data in data:
            product_info[product_data] = data.get(product_data, None)
            print(product_data)
        origin_brands = []
        print(product_info, "@@@@@@@@@@@@")
        brands = product_info.get('brands', None)
        brands_list = [int(brand)
                       for brand in brands.split(',') if brand.isdigit()]
        print(brands_list)
        origin_brands = storeBrands.objects.filter(
            partSupplierId=part_supplier.pk, brands__in=brands_list)
        #     brands_list = brands.split(',')
        #     for brand in brands_list:
        #         b = Brand.objects.filter(id=brand).first()
        #         a = int(brand)
        #         print(type(a))
        #         print(brands)
        #         print(b)
        #         if b:
        #             origin_brands = storeBrands.objects.filter(
        #                 partSupplierId=part_supplier.pk, brands=[16, 17])
        print(origin_brands.count(), brands_list.__len__())
        if origin_brands.count() == brands_list.__len__():
            for i in origin_brands:
                product_info["brands"] = i.brands.pk
                print(i.brands.pk)
                print(product_info)
                product = ProductPartSupplierSerializer(data=product_info)
                product.is_valid(raise_exception=True)
                product.save()

        return Response(origin_brands.values(), status=status.HTTP_200_OK)


class CarModelViewSet(ModelViewSet):

    # pagination_class = StandardResultsSetPagination
    queryset = CarModel.objects.filter()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand']


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all().order_by('pk')
    serializer_class = StoreSerializer
    # permission_classes = [IsAuthenticated, workshopOwnerAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin']

    def create(self, request, *args, **kwargs):
        print('wwww')
        # TODO BTING ID FORM REQUEST AND ADD IT TO DATA
        request.data._mutable = True
        user = self.request.user.pk
        print(request.data)
        print("a")
        ShopOwner = PartSupplier.objects.get(user_id=user)
        print(ShopOwner)
        print("1!!!")
        request.data["partSupplierId"] = ShopOwner.pk
        print('1')
        return super().create(request, *args, **kwargs)


class CarOwnerUpdateAPIView(APIView):
    def put(self, request, pk, *args, **kwargs):
        car_owner = CarOwner.objects.get(user_id=pk)
        user = car_owner.user_id

        user.avatar = request.data.get('avatar', user.avatar)
        user.email = request.data.get('email', user.email)
        user.fullName = request.data.get('fullName', user.fullName)
        user.set_password(request.data.get('password', user.password))
        user.phoneNumber = request.data.get('phoneNumber', user.phoneNumber)

        user.save()

        return Response(status=status.HTTP_200_OK)


class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


@api_view(['GET', 'POST'])
def add(request):
    cars = {
        "Germany": [
            "BMW",
            "Mercedes-Benz",
            "Audi",
            "Opel",
            "Volkswagen",
            "Porsche"
        ],
        "USA": [
            "Ford",
            "Chevrolet",
            "Tesla",
            "Dodge",
            "Jeep",
            "GMC",
            "polaris",
            "Chrysler",
            "Cadillac"
        ],
        "Japan": [
            "Toyota",
            "Honda",
            "Nissan",
            "Mazda",
            "Subaru"
        ],
        "South Korea": [
            "Hyundai",
            "Kia",
            "Genesis",
            "Samsung",
            "SsangYong"
        ],
        "Italy": [
            "Ferrari",
            "Lamborghini",
            "Maserati",
            "Alfa Romeo",
            "Fiat"
        ],
        "Spain": [
            "SEAT",
            "Cupra",
            "Pegaso",
            "Hispano-Suiza",
            "GTA Motor"
        ],
        "UK": [
            "Jaguar",
            "Land Rover",
            "Aston Martin",
            "Rolls-Royce",
            "Bentley"
        ],
        "Iran": [

            "Iran Khodro",
            "Saipa",
            "Kish Khodro",
            "Pars Khodro",
            "Bahman Group"
        ],
        "China": [
            "Geely",
            "BYD",
            "Changan",
            "Great Wall",
            "SAIC Motor"
        ],

        "France": [
            "Peugeot",
            "Renault",
            "Citroen",
            "Bugatti",
            "DS Automobiles"
        ]

    }

    for i in cars:
        for x in cars[i]:
            ori = Brand(name=x, origin=origin.objects.get(name=i))
            print(ori)
            ori.save()
    return Response()


class locationsViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def workShop(request):
    work = WorkShop.objects.all()

    return Response(type)


@api_view(['GET'])
def userType(request):
    type = {"type": ['Workshop Owner', 'Car Owner',
                     'Parts Supplier', 'Tow Car Owner']}
    return Response(type)


@api_view(['POST'])
def AddSpecialist(request):
    specialist_type = [
        "Motor",  # path('AddSpecialist', views.AddSpecialist)
        "Electric",
        "Body",
        "Suspension",

    ]

    for i in specialist_type:
        ori = Specialist(name=i)
        print(ori)
        ori.save()
    return Response()


@api_view(['POST'])
def AddOrigin(request):
    origin_type = [
        "Germany",
        "Japan",
        "USA",
        "UK",
        "Italy",
        "Spain",
        "South Korea",
        "China",
        "Iran",
        "France"
    ]

    for i in origin_type:
        ori = origin(name=i)
        print(ori)
        ori.save()
    return Response()


@api_view(['POST'])
def AddTowOrigin(request):
    origin_type = [
        "Germany",
        "Japan",
        "USA",
        "UK",
        "Italy",
        "Spain",
        "South Korea",
        "China",
        "Iran",
        "Sweden"
    ]

    for i in origin_type:
        ori = TowOrigin(name=i)
        print(ori)
        ori.save()
    return Response()


@api_view(['POST'])
def AddTowBrand(request):
    cars = {
        "Germany": [
            "Mercedes-Benz"],
        "USA": [
            "Ford",

        ],
        "Italy": [
            "Fiat",],
        "Sweden": [
            "Volvo",],

    }

    for i in cars:

        for x in cars[i]:
            print("11111111111111111111111")
            ori = TowBrand(
                name=x, origin=TowOrigin.objects.get(name=i))
            ori.save()
    return Response()


@api_view(['POST'])
def AddCity(request):
    origin_type = [
        "Aleppo",
        "Lattakia",
        "Homs",
        "Hama",
        "Tartus",
        "Daraa",
        "Rif Dimashq",
        "Daraa",
        "Quneitra",
        "Raqqa",
        "Damascus ",

    ]

    for i in origin_type:
        ori = City(name=i)
        print(ori)
        ori.save()
    return Response()


@api_view(['POST'])
def AddProduct(request):
    origin_type = {"Motor": [
        "Engine",
        "Gear Box",
        "Fuel system",
        "Steering system",
        "Ignition system",
        "Exhaust system",
        "Axles",
        "Drive shaft",
        "Radiator",
        "Filters (air)",
        "Filters (fuel)",
        "Filters (oil)",
        "Battery",],
        "Body": [
        "Front Light",
        "Front Pumper",
        "Back Pumper",
        "Door",
        "Belts",],
        "Electric": [
        "Electrical system",
        "Alternator",
        "Hoses",],
        "Suspension": [
        "Transmission",
        "Brakes",
        "Suspension system",]


    }

    for i in origin_type:
        for x in origin_type[i]:
            ori = Product(
                productName=x, category=Specialist.objects.get(name=i))
            ori.save()

        print(i)
        print(origin_type[i])
    return Response()


@api_view(['POST'])
def AddCarModel(request):
    brand = {"Toyota": [
        "camry",
        "corolla",
        "yaris",
        "prius",
        "rav4",
        "highlander",
        "land cruiser"
    ],
        "Honda": [
        "civic",
        "accord",
        "cr-v",
        "odyssey",
        "pilot",
        "fit",
        "hr-v",
        "insight",
        "passport"
    ],
        "Ford": [
        "f-150",
        "mustang",
        "explorer",
        "edge",
        "ranger",
        "fusion",
        "focus",
    ],
        "Chevrolet": [
        "silverado",
        "malibu",
        "impala",
        "corvette",
        "Camaro",
        "spark",
        "suburban",
        "tahoe"
    ],
        "Nissan": [
        "altima",
        "maxima",
        "sentra",
        "pathfinder",
        "titan",
        "frontier"
        "armada"
    ],

        "BMW": [
        "1 Series",
        "2 Series",
        "3 Series",
        "4 Series",
        "5 Series",
        "6 Series",
        "7 Series",
        "8 Series",
        "X1",
        "X2",
        "X3",
        "X4",
        "X5",
        "X6",
        "Z4",
        "i3",
        "i8",
        "M4"
    ],
        "Mercedes-Benz": [
        "C-Class",
        "E-Class",
        "S-Class",
        "GLA-Class",
        "GLC-Class",
        "GLE-Class",
        "GLS-Class",
        "AMG GT",
        "SL-Class",
        "G-Class"
    ],
        "Audi": [
        "A3",
        "A4",
        "A5",
        "A6",
        "Q3",
        "Q5",
        "Q7",
        "TT",
        "R8",
        "S5"
    ],
        "Opel": [
        "Corsa",
        "Omega",
        "Astra",

    ],
        "Volkswagen": [
        "Golf",
        "Passat",
        "Tiguan",
        "T-Roc",
        "T-Cross",
        "Arteon",
        "Touran",
        "Sharan",
        "Transporter",
        "Caddy"
    ],
        "Porsche": [
        "911",
        "Cayman",
        "Boxster",
        "Panamera",
        "Macan",
        "Cayenne",
        "Taycan",
        "718",
        "911 GT2 RS",
        "911 Turbo S"
    ],
        "Tesla": [
        "Model S",
        "Model 3",
        "Model X",
        "Model Y",
        "Roadster",
    ],
        "Dodge": [
        "Charger",
        "Challenger",
        "Durango",
        "Journey",
        "Grand Caravan",
        "Ram 1500",
        "Ram 2500",
        "Ram 3500",
        "Viper",
        "Dakota"
    ],
        "Jeep": [
        "Wrangler",
        "Grand Cherokee",
        "Cherokee",
        "Compass",
        "Renegade",
        "Gladiator",
        "Commander",
        "Patriot",
        "Liberty",
        "Wagoneer"
    ],
        "GMC": [
        "Sierra",
        "Acadia",
        "Terrain",
        "Yukon",
        "Canyon",
    ],
        "Hyundai": [
            "Sonata",
            "Elantra",
            "Tucson",
            "Santa Fe"
    ],
        "Kia": [
            "Optima",
            "Soul",
            "Sportage",
            "Sorento",
            "Stinger"
    ],
        "Genesis": [
            "G70",
            "G80",
            "G90",
            "GV70",
            "GV80"
    ],
        "Samsung": [
            "SM3",
            "SM5",
            "SM6",
            "SM7",
            "QM6"
    ],
        "SsangYong": [
            "Tivoli",
            "Korando",
            "Rexton",
            "Musso",
            "Rodius"
    ],


        "Ferrari": [
            "488 GTB",
            "Portofino",
            "F8 Tributo",
            "SF90 Stradale",
            "Roma"
    ],
        "Lamborghini": [
            "Aventador",
            "Huracán",
            "Urus",
            "Sian",
            "Essenza SCV12"
    ],
        "Maserati": [
            "Ghibli",
            "Quattroporte",
            "Levante",
            "GranTurismo",
            "MC20"
    ],
        "Alfa Romeo": [
            "Giulia",
            "Stelvio",
            "Giulietta",
            "4C Spider",
            "Tonale"
    ],
        "Fiat": [
            "500",
            "Panda",
            "Tipo",
            "124 Spider",
            "500X"
    ],
        "SEAT": [
            "Leon",
            "Ibiza",
            "Ateca",
            "Arona",
            "Tarraco"
    ],
        "Cupra": [
            "Leon",
            "Formentor",
            "Ateca"
    ],
        "Jaguar": [
            "F-Type",
            "XE",
            "XF",
            "XJ",
            "F-PACE"
    ],
        "Land Rover": [
            "Range Rover",
            "Range Rover Sport",
            "Range Rover Velar",
            "Defender",
            "Discovery"
    ],
        "Aston Martin": [
            "DB11",
            "Vantage",
            "DBS Superleggera",
            "Rapide AMR",
            "Valhalla"
    ],
        "Rolls-Royce": [
            "Phantom",
            "Ghost",
            "Wraith",
            "Dawn",
            "Cullinan"
    ],
        "Bentley": [
            "Continental GT",
            "Flying Spur",
            "Bentayga",
            "Mulsanne",
            "Bacalar"
    ],
        "Geely": [
            "Emgrand X7",
            "Bo Rui",
            "Coolray",
            "Vision X3",
            "Atlas Pro"
    ],
        "BYD": [
            "Tang",
            "Han",
            "Song Plus",
            "Yuan",
            "e2"
    ],
        "Changan": [
            "CS75 Plus",
            "CS35 Plus",
            "CS55 Plus",
            "CS95",
            "UNI-T"
    ],
        "Great Wall": [
            "Haval H6",
            "Haval H9",
            "Haval F7",
            "Wey VV7",
            "Wingle 7"
    ],
        "SAIC Motor": [
            "MG ZS",
            "Roewe RX5",
            "Maxus G50",
            "LDV T60",
            "Baojun 530"
    ],
        "Peugeot": [
            "208",
            "308",
            "3008",
            "5008",
            "Partner"
    ],
        "Renault": [
            "Clio",
            "Megane",
            "Captur",
            "Kadjar",
            "Talisman"
    ],
        "Citroen": [
            "C3",
            "C4",
            "C5 Aircross",
            "Berlingo",
            "Jumpy"
    ],
        "Bugatti": [
            "Chiron",
            "Divo",
            "Centodieci",
            "La Voiture Noire",
            "Veyron"
    ],
        "DS Automobiles": [
            "DS 3 Crossback",
            "DS 7 Crossback",
            "DS 9",
            "DS 4",
            "DS 5"
    ]}

    for i in brand:
        for x in brand[i]:
            print("11111111111111111111111")
            ori = CarModel(
                name=x, brand=Brand.objects.get(name=i))
            ori.save()
        print(i)
        print(brand[i])
    return Response()
