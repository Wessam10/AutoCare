from django.shortcuts import render
from rest_framework .viewsets import ModelViewSet, generics
from django.shortcuts import get_object_or_404
from .models import User, CarOwner, PartSupplier, TowCarOwner, WorkShopOwner, product, TowRequest, origin, Brand, location, Cars, WorkShop, Request, maintenance, checkup
from .Serializer import WorkShopSerializer,  UserImageSerializer, RequestSerializer, BrandSerializer, CarOwnerSerializer, CarsSerializer, checkupSerializer, locationSerializer, maintenanceSerializer, OriginSerializer, PartSupplierSerializer, productSerializer, TowCarOwnerSerializer, TowRequestSerializer, WorkShopOwnerSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


def responseData(data: dict, status: bool, message: str):
    response = {'data': data, 'status': status, 'message': message}
    return response


class WorkShopViewSet (ModelViewSet):
    queryset = WorkShop.objects.all().order_by('pk')
    serializer_class = WorkShopSerializer
    permission_classes = [IsAuthenticated]


class RequestViewSet (ModelViewSet):
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]


class BrandViewSet (ModelViewSet):
    queryset = Brand.objects.all().order_by('pk')
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]


class CarOwnerViewSet (ModelViewSet):
    queryset = CarOwner.objects.all().order_by('pk')
    serializer_class = CarOwnerSerializer
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
    permission_classes = [IsAuthenticated]


class PartSupplierViewSet (ModelViewSet):
    queryset = PartSupplier.objects.all().order_by('pk')
    serializer_class = PartSupplierSerializer
    permission_classes = [IsAuthenticated]


class productViewSet (ModelViewSet):
    queryset = product.objects.all().order_by('pk')
    serializer_class = productSerializer
    permission_classes = [IsAuthenticated]


class TowCarOwnerViewSet (ModelViewSet):
    queryset = TowCarOwner.objects.all().order_by('pk')
    serializer_class = TowCarOwnerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user_id
        serializer = TowCarOwnerSerializer
        car = User.objects.filter(id=user)
        if car.exists:
            serializers = TowCarOwnerSerializer(data=car)
            print(serializers.data)
            return Response(responseData(data=serializer.data, message='User info', status=True), status=status.HTTP_200_OK)
        else:
            return Response(responseData(data=None, message='Invalid data', status=False), status=status.HTTP_200_OK)


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
        queryset = User.objects.all()
        serializer = WorkShopOwnerSerializer(queryset)
        user = request.user_id
        workshop = User.objects.filter(id=user)
        if workshop.exists:
            serializers = WorkShopOwnerSerializer(data=workshop)
            return Response(responseData(data=serializer.data, message='User info', status=True), status=status.HTTP_200_OK)
        else:
            return Response(responseData(data=None, message='Invalid data', status=False), status=status.HTTP_200_OK)


class OriginViewSet (ModelViewSet):
    queryset = origin.objects.all().order_by('pk')
    serializer_class = OriginSerializer
    permission_classes = [IsAuthenticated]


class CheckupViewSet (ModelViewSet):
    queryset = checkup.objects.all().order_by('pk')
    serializer_class = checkupSerializer
    permission_classes = [IsAuthenticated]


class locationViewSet (ModelViewSet):
    queryset = location.objects.all().order_by('pk')
    serializer_class = locationSerializer
    permission_classes = [IsAuthenticated]


class MaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer
    permission_classes = [IsAuthenticated]


class userImagesViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        print(request.user, '22222222222222222222224222222222222222')
        user = request.user_id
        userImage = User.objects.filter(id=user)
        if userImage.exists:
            serializers = UserSerializer(data=userImage)
            print(UserSerializer)
            return Response(responseData(data=userImage, message='image retrieved', status=True), status=status.HTTP_200_OK)
        else:
            return Response(responseData(data=None, message='there is no one ', status=False), status=status.HTTP_200_OK)
