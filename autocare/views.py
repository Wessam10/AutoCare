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

from . import models
from .models import (Brand, CarOwner, Cars, PartSupplier, Request, Specialist,
                     TowCarOwner, TowRequest, User, WorkShop, WorkShopImages,
                     WorkShopOwner, checkup, location, maintenance, origin, City, ProductPartSupplier,
                     product, TowCar)
from .permission import CarOwnerAuth, workshopOwnerAuth, PartSupplierAuth, TowCarOwnerAuth
from .Serializer import (BrandSerializer, CarOwnerSerializer, CarsSerializer,
                         OriginSerializer, PartSupplierSerializer,
                         RequestSerializer, TowCarOwnerSerializer,
                         TowRequestSerializer, UserImageSerializer,
                         UserSerializer, WorkShopImageSerializer,
                         WorkShopOwnerSerializer, WorkShopSerializer,
                         checkupSerializer, locationSerializer,
                         maintenanceSerializer, productSerializer, TowCarSerializer, specialistSerializer, ProductPartSupplierSerializer, MyTokenObtainPairSerializer)
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


class WorkShopViewSet (ModelViewSet):
    queryset = WorkShop.objects.all().order_by('pk')
    serializer_class = WorkShopSerializer
    # permission_classes = [IsAuthenticated, workshopOwnerAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin']

    def create(self, request, *args, **kwargs):
        print('wwww')
        # TODO BTING ID FORM REQUEST AND ADD IT TO DATA
        request.data._mutable = True
        user = request.user.pk
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

    def create(self, request, *args, **kwargs):
        print('aaaa')
        request.data._mutable = True
        user = request.user.pk
        carOwner = CarOwner.objects.get(user_id=user)
        print(user)
        request.data["userId"] = carOwner.pk
        print('aaaa')

        return super().create(request, *args, **kwargs)


class PartSupplierViewSet (ModelViewSet):
    queryset = PartSupplier.objects.all().order_by('pk')
    serializer_class = PartSupplierSerializer
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
        print(user_instance)
        request.data["user_id"] = user_instance.pk

        return super().create(request, *args, **kwargs)


class productViewSet (ModelViewSet):
    queryset = product.objects.all().order_by('pk')
    serializer_class = productSerializer
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

            'user': workshopUser.pk,


            'user_info': user_info
        }

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

            'user': workshopUser.pk,


            'user_info': user_info
        }

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)


class OriginViewSet (ModelViewSet):
    queryset = origin.objects.all().order_by('pk')
    serializer_class = OriginSerializer
    permission_classes = [IsAuthenticated]


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
        user = self.queryset.get(pk=request.user.pk)
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
        user_id = request.user.pk
        print(user_id)
        workshops = WorkShop.objects.get(workshopOwnerId__user_id=user_id)
        workshop_id = workshops.pk
        print(workshop_id)
        request.data['WorkShop'] = workshop_id
        print(dict(request.data))
        # print(request.data['WorkShop'])
        return super().create(request, *args, **kwargs)


class TowCarViewSet(ModelViewSet):
    queryset = TowCar.objects.filter()
    serializer_class = TowCarSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request_data = request.data
        user = request.user.pk
        request.data["userId"] = user
        towCar_info = {}
        for user_data in request_data:
            print(user_data)
            towCar_info[user_data] = request_data.get(user_data, None)
        print(towCar_info)
        car = CarsSerializer(data=towCar_info)
        car.is_valid(raise_exception=True)
        workshopUser = car.save()
        print(workshopUser)
        request_data["car_id"] = workshopUser.pk

        return super().create(request, *args, **kwargs)


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
            product.favorite.remove(request.user)
        else:
            product.favorite.add(request.user)

    def retrieve(self, request, *args, **kwargs):
        user = request.user_id
        favorite = WorkShop.favorite.all()
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductPartViewSet (ModelViewSet):
    queryset = ProductPartSupplier.objects.filter()
    serializer_class = ProductPartSupplierSerializer
    permission_classes = [IsAuthenticated, PartSupplierAuth]
    # for brand_string in brands_data[0].split(','):
    #     print(brand_string)
    #     shopBrands = workshopBrandsSerializer(
    #         data={'workshop': workshop.pk, 'brands': brand_string})

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data.pk
        user = request.user.pk
        pro = product.object.get(id=data)
        print(user)
        request.data['partSupplierId'] = user
        product_info = {}
        print('1')
        for product_data in data:
            print(product_data)
            product_info[product_data] = data.get(product_data, None)
        print(product_info)
        product = ProductPartSupplierSerializer(data=product_info)
        product.is_valid(raise_exception=True)
        workshopUser = product.save()

        return super().create(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def add(request):
    cars = {
        "Germany": [
            "BMW",
            "Mercedes-Benz",
            "Audi",
            "Volkswagen",
            "Porsche",
            "Opel",
            "Mini",
            "Smart",
            "Maybach",
            "Volkswagen (VW)",
            "Porsche",
            "Audi",
            "BMW",
            "Mercedes-AMG",
            "MAN",
            "Wiesmann",
            "Borgward",
            "Gumpert",
            "Ruf Automobile",
            "Brabus"
        ],
        "USA": [
            "Ford",
            "Dodge",
            "GMC",
            "Jeep",
            "TESLA",
            "CHRYSLER",
            "CHEVROLET",
            "POLARIS",
            "Cadillac",]

    }

    for i in cars["Germany"]:
        ori = Brand(name=i, origin=origin.objects.get(name='Germany'))
        print(ori)
        ori.save()
    return Response()


class locationsViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        "Japan",
        "USA",
        "UK",
        "Italy",
        "Spain",
        "South Korea",
        "China",
        "Iran"
    ]

    for i in origin_type:
        ori = origin(name=i)
        print(ori)
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
    origin_type = [
        "Front Light",
        "Front Pumper",
        "Back Pumper",
        "Engine",
        "Door",
        "Gear Box",
        "Transmission",
        "Brakes",
        "Suspension system",
        "Exhaust system",
        "Fuel system",
        "Electrical system",
        "Battery",
        "Radiator",
        "Alternator",
        "Ignition system",
        "Steering system",
        "Drive shaft",
        "Axles",
        "Wheels",
        "Tires",
        "Belts",
        "Hoses",
        "Filters (air)"
        "Filters (oil)"
        "Filters (fuel)"


    ]

    for i in origin_type:
        ori = product(productName=i)
        print(ori)
        ori.save()
    return Response()
