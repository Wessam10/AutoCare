from django.shortcuts import render
from rest_framework .viewsets import ModelViewSet, generics
from django.shortcuts import get_object_or_404
from .models import User, WorkShopImages, CarOwner, PartSupplier, TowCarOwner, WorkShopOwner, product, TowRequest, origin, Brand, location, Cars, WorkShop, Request, maintenance, checkup, Specialist
from .Serializer import MyTokenObtainPairSerializer, WorkShopSerializer,  WorkShopImageSerializer, UserImageSerializer, RequestSerializer, BrandSerializer, CarOwnerSerializer, CarsSerializer, checkupSerializer, locationSerializer, maintenanceSerializer, OriginSerializer, PartSupplierSerializer, productSerializer, TowCarOwnerSerializer, TowRequestSerializer, WorkShopOwnerSerializer, UserSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view
from . import models
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .permission import CarOwnerAuth, workshopOwnerAuth
# C:\Users\MAVERICK\Documents\HRMS\AutoCareCar


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def responseData(data: dict, status: bool, message: str):
    response = {'data': data, 'status': status, 'message': message}
    return response


class WorkShopViewSet (ModelViewSet):
    queryset = WorkShop.objects.all().order_by('pk')
    serializer_class = WorkShopSerializer
    # permission_classes = [IsAuthenticated, workshopOwnerAuth]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['origin']

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
    permission_classes = [IsAuthenticated]


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
        request.data._mutable = True
        user = request.user.pk
        print(user)
        request.data["userId"] = user
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
    permission_classes = [IsAuthenticated]


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
        for user_data in request_data:
            print(user_data)
            user_info[user_data] = request_data.get(user_data, None)

        user = UserSerializer(data=user_info)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        request_data["user_id"] = workshopUser.pk
        print('aaaa')
        return super().create(request, *args, **kwargs)


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
    # permission_classes = [IsAuthenticated]

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
        for user_data in request_data:
            print(user_data)
            user_info[user_data] = request_data.get(user_data, None)

        user = UserSerializer(data=user_info)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        print(workshopUser)
        request_data["user_id"] = workshopUser.pk
        print('done')
        return super().create(request, *args, **kwargs)


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


@api_view(['GET', 'POST'])
def add(request):
    cars = {"Germany": [
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
    ]
    }

    for i in cars['Germany']:
        ori = Brand(name=i, origin=origin.objects.get())
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


@api_view(['GET'])
def GetSpecialist(request):
    type = {"specialists": ['Motor', 'Electric',
                            'Body', 'Suspension']}
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
