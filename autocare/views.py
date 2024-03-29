import http.client
import json
import jwt
from django.contrib.auth.models import User
from django.conf import settings
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
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
import math
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import APIException
from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from .permission import CarOwnerAuth, workshopOwnerAuth, PartSupplierAuth, TowCarOwnerAuth
from .models import (User, Brand, CarOwner, Cars, PartSupplier, Request, Specialist,
                     TowCarOwner, TowRequest, User, WorkShop, WorkShopImages, workshopBrands,
                     WorkShopOwner, checkup, location, maintenance, Origin, City, ProductPartSupplier,
                     Product, TowCars, CarModel, TowBrand, TowOrigin, storeBrands, Images, Store, Status, TransactionStatus, RequestType)
from .Serializer import (BrandSerializer, CarOwnerSerializer, CarsSerializer, TowBrandSerializer, TowOriginSerializer,
                         OriginSerializer, PartSupplierSerializer,
                         RequestSerializer, TowCarOwnerSerializer,
                         TowRequestSerializer, UserImageSerializer,
                         UserSerializer, WorkShopImageSerializer,
                         WorkShopOwnerSerializer, WorkShopSerializer,
                         checkupSerializer, locationSerializer,
                         maintenanceSerializer, productSerializer, WPartSupplierSerializer, ImagesSerializer, RequestTypeSerializer, TransactionStatusSerializer, StatusSerializer, CitySerializer, TowCarsSerializer, StoreSerializer, storeBrandsSerializer, CarModelSerializer, specialistSerializer, ProductPartSupplierSerializer, MyTokenObtainPairSerializer)
# C:\Users\MAVERICK\Documents\HRMS\AutoCareCar


def responseData(data: dict, status: bool, message: str):
    response = {'data': data, 'status': status, 'message': message}
    return response


# def custom_exception_handler(exc, context):
#     # Customize error response based on exception type
#     if isinstance(exc, ValidationError):
#         response = Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         response = Response("An error occurred",
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     logger = logging.getLogger(__name__)
#     # Log the error for debugging
#     logger.error(f"Error: {exc}")
#     return response


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
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
        queryset1 = workshopBrands.objects.none()  # Initialize as an empty queryset
        if brand_name:
            queryset1 = workshopBrands.objects.filter(brands=brand_name)
            print(queryset1.values_list("workshop", flat=True))
            if not queryset1.exists():
                raise NotFound("Workshops not found for the specified brand.")
            print(queryset1)
        if queryset1.exists():
            result = WorkShop.objects.filter(
                id__in=queryset1.values_list("workshop", flat=True))
        else:
            result = queryset
        print(result.values_list("origin", flat=True))
        return result

    # def get_queryset(self):
    #     user_id = self.request.user.pk
    #     try:
    #         car_owner = CarOwner.objects.get(user_id=user_id)
    #         return Cars.objects.filter(userId=car_owner.pk).order_by('pk')
    #     except CarOwner.DoesNotExist:
    #         raise NotFound("Car owner not found.")

    def create(self, request, *args, **kwargs):
        user = self.request.user.pk
        shop_owner = WorkShopOwner.objects.get(user_id=user)

    # Check if the shop owner already has a workshop
        if WorkShop.objects.filter(workshopOwnerId=shop_owner.pk).exists():
            return Response("You already have a workshop and cannot create another.", status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
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
    filterset_fields = ['userId', 'requestType', 'status', 'transactionStatus']

    def get_queryset(self):
        user_id = self.request.user.pk
        owner = WorkShopOwner.objects.get(user_id=user_id)
        shop = WorkShop.objects.filter(workshopOwnerId=owner).first()
        return Request.objects.filter(workshopId=shop).order_by('pk').exclude(transactionStatus=6)


class workShopRequestViewSet (ModelViewSet):
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'requestType', 'status', 'transactionStatus']


class CarOwnerRequestViewSet (ModelViewSet):
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'requestType', 'status', 'transactionStatus']

    def get_queryset(self):
        user_id = self.request.user.pk
        owner = CarOwner.objects.get(user_id=user_id)
        return Request.objects.filter(userId=owner.pk).order_by('pk')


class ExcludeRequestViewSet(ModelViewSet):
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    # permission_classes = [IsAuthenticated]  # Uncomment for permission control
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId', 'requestType',
                        'status']  # Remove 'transactionStatus'

    def get_queryset(self):
        user_id = self.request.user.pk
        owner = CarOwner.objects.get(user_id=user_id)
        queryset = Request.objects.filter(userId=owner.pk)

        queryset = Request.objects.filter(
            userId=owner.pk).exclude(transactionStatus=6)

        return queryset


class CurrentCarsViewSet (ModelViewSet):
    # pagination_class = StandardResultsSetPagination
    queryset = Request.objects.all().order_by('pk')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workshopId', 'transactionStatus']

    def get_queryset(self):
        user_id = self.request.user.pk
        owner = WorkShopOwner.objects.get(user_id=user_id)
        shop = WorkShop.objects.filter(workshopOwnerId=owner).first()
        print(shop)
        k = Request.objects.filter(
            workshopId=shop.pk).order_by('pk')
        print(k)
        return k


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
        user.is_valid()
        if user.errors:
            print(user.errors)
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
    filterset_fields = ['origin']
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_name = self.request.query_params.get('brands')
        print(brand_name)
        queryset1 = storeBrands.objects.none()  # Initialize as an empty queryset
        if brand_name:
            queryset1 = storeBrands.objects.filter(brands=brand_name)
            print('quer')
            print(queryset1)
            print(queryset1.values_list("partSupplierId", flat=True))
            print('quer')
            if not queryset1.exists():
                print('quer')
                raise NotFound(
                    "PartSupplier not found for the specified brand.")
                print(queryset1)
        if queryset1.exists():
            result = PartSupplier.objects.filter(
                id__in=queryset1.values_list("partSupplierId", flat=True))
        else:
            result = queryset
        print(result.values_list("origin", flat=True))
        return result

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
        user.is_valid()
        if user.errors:
            print(user.errors)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        print('aaaa')
        print(user_instance.pk)
        request.data["user_id"] = user_instance.pk
        us = User.objects.get(id=user_instance.pk)
        token_serializer = MyTokenObtainPairSerializer()
        token = token_serializer.get_token(us)

        k = self.get_serializer(data=request_data)
        k.is_valid(raise_exception=True)

        if k.errors:
            print(k.errors)
        k.is_valid()
        print('@@@@@!!!!',  k.is_valid())
        k.save()
        print('@@@@@!!!!')
        # Include the token in the response data
        response_data = {
            'token': str(token.access_token),

            'user': user_instance.pk
        }

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)


class brandStoreViewSet (ModelViewSet):
    queryset = storeBrands.objects.all().order_by('pk')
    serializer_class = storeBrandsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partSupplierId', 'brands']
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        u = PartSupplier.objects.get(user_id=user.pk)
        queryset = storeBrands.objects.filter(partSupplierId=u.pk)
        return queryset


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
        user.is_valid()
        if user.errors:
            print(user.errors)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        print(workshopUser)
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


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Earth's radius in kilometers
    radius = 6371

    # Apply Haversine formula
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


class TowRequestViewSet (ModelViewSet):
    queryset = TowRequest.objects.all().order_by('pk')
    serializer_class = TowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            requests = Request.objects.filter(userId=user.pk)
            return TowRequest.objects.filter(requestId__in=requests).order_by('pk')
        else:
            return TowRequest.objects.all().order_by('pk')

    @action(detail=False, methods=['get'])
    def get_distance_for_all_cars(self, request):
        """
        Calculates and returns the distances to all available tow cars from the provided location.

        Raises:
            ValueError: If the 'currentLocation' is missing or invalid in the request data.
            AttributeError: If a tow car has no location attribute.
        """

        try:
            # Validate and extract coordinates from request data
            coordinates1 = request.data.get('currentLocation', '').strip()
            if not coordinates1:
                raise ValueError(
                    "'currentLocation' is required in the request data.")
            latitude1, longitude1 = coordinates1.split(',')
            latitude1 = float(latitude1)
            longitude1 = float(longitude1)

            # Get all available tow cars
            tow_cars = TowCars.objects.filter(available=True).order_by('pk')

            distances = []
            R = 6371  # Radius of the Earth in kilometers

            # Convert coordinates to radians and calculate distance for each tow car
            for i in tow_cars:
                # Check for missing location
                if not i.location:
                    # Handle tow car with no location (e.g., log or skip)
                    print(f"Tow car with ID {i.id} has no location.")
                    continue

                latitude2, longitude2 = map(float, i.location.split(','))
                lat1_rad = math.radians(latitude1)
                lon1_rad = math.radians(longitude1)
                lat2_rad = math.radians(latitude2)
                lon2_rad = math.radians(longitude2)

                delta_lat = lat2_rad - lat1_rad
                delta_lon = lon2_rad - lon1_rad

                a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * \
                    math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c

                distances.append({'tow_car_id': i.id, 'distance': distance})

            sorted_distances = sorted(distances, key=lambda x: x['distance'])
            distances_list = [{'tow_car_id': item['tow_car_id'], 'distance': item['distance'], 'location': TowCars.objects.get(
                id=item['tow_car_id']).location} for item in sorted_distances]

            return Response(distances_list)

        except (ValueError, AttributeError) as e:
            # Handle validation errors and missing attributes gracefully
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        user = self.request.user.pk
        print('1234', self.get_distance_for_all_cars(
            request).data[0]['tow_car_id'])
        sorted_distances = self.get_distance_for_all_cars(
            request).data
        print(sorted_distances[0])
        request.data["towCarId"] = sorted_distances[0]['tow_car_id']
        print(user)
        request_data = request.data
        carOwner = CarOwner.objects.get(user_id=user)
        towOwner = sorted_distances[0]['tow_car_id']
        print(towOwner)
        us = TowCars.objects.get(id=towOwner)
        k = us.userId.user_id
        try:
            devices = FCMDevice.objects.get(user_id=k.pk)
            print(devices.registration_id)
            print('ppppppppppppppppppppppppppppppppppppppppp')
            conn = http.client.HTTPSConnection("fcm.googleapis.com")
            print(devices.registration_id, 'ddddddddddddddddddddddddddd')
            payload = json.dumps({
                "to": devices.registration_id,
                "notification": {
                    "title": "New Request",
                    "body": "You have new Tow Request",
                    "mutable_content": True,
                    "sound": "Tri-tone"
                },

            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
            }
            conn.request("POST", "/fcm/send", payload, headers)
            res = conn.getresponse()
            data = res.read()
        except FCMDevice.DoesNotExist:
            # Handle case where no device token is found
            print("No device token found for workshop owner")
            return Response({"message": "No device token found for TowCar "}, status=status.HTTP_400_BAD_REQUEST)

        request.data["userId"] = carOwner.pk

        request_info = {}

        for data in request_data:
            print(data)
            request_info[data] = request_data.get(data, None)

        serializer = RequestSerializer(data=request_info)
        serializer.is_valid()
        if serializer.errors:
            print(serializer.errors)
        serializer.is_valid(raise_exception=True)
        r1 = serializer.save()

        request_data["requestId"] = r1.pk
        request_data
        print(request_data)
        k = TowRequestSerializer(data=request_data,)
        k.is_valid()
        if k.errors:
            print(k.errors)
        k.is_valid()
        k.save()
        print(k.is_valid())

        return Response(request.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        user = self.request.user.pk
        request.data._mutable = True
        shop = Request.objects.get(id=request_id)
        k = shop.userId.user_id
        mai = TowRequest.objects.get(requestId=shop.pk)
        s = int(request.data.get('status', ''))
        print(s)
        if s == 3 or s == 4:
            request.data["transactionStatus"] = 6
        else:
            request.data["transactionStatus"] = 5
        try:
            devices = FCMDevice.objects.get(user_id=k.pk)
            print(devices.registration_id)
            print('ppppppppppppppppppppppppppppppppppppppppp')
            conn = http.client.HTTPSConnection("fcm.googleapis.com")
            print(devices.registration_id, 'ddddddddddddddddddddddddddd')
            payload = json.dumps({
                "to": devices.registration_id,
                "notification": {
                    "title": "New Request",
                    "body": "Check Request info",
                    "mutable_content": True,
                    "sound": "Tri-tone"
                },

            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
            }
            conn.request("POST", "/fcm/send", payload, headers)
            res = conn.getresponse()
            data = res.read()
        except FCMDevice.DoesNotExist:
            # Handle case where no device token is found
            print("No device token found for workshop owner")
            return Response({"message": "No device token found for workshop owner"}, status=status.HTTP_400_BAD_REQUEST)
        lat1_str, lon1_str = mai.currentLocation.split(',')
        lat2_str, lon2_str = mai.destination.split(',')
        lat1 = float(lat1_str)
        lon1 = float(lon1_str)
        lat2 = float(lat2_str)
        lon2 = float(lon2_str)
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        print('v')
        c = distance * 10000
        cost_int = int(c)
        print(c)
        print(cost_int)
        request.data["userId"] = shop.userId.pk
        request.data["carsId"] = shop.carsId.pk
        print(shop.pk)
        request.data["currentLocation"] = mai.currentLocation
        request.data["destination"] = mai.destination
        request.data['requestId'] = request_id
        request.data['requestType'] = shop.requestType

        request.data['cost'] = cost_int
        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        print(shop)
        serializer.is_valid(raise_exception=True)

        serializer.update(instance=shop,
                          validated_data=serializer.validated_data)
        k = TowRequestSerializer(
            instance=mai, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=mai, validated_data=k.validated_data)
        print('123578910')

        return Response(k.data, status=status.HTTP_200_OK)


class tokenDeviceViewSet (ModelViewSet):
    queryset = TowRequest.objects.all().order_by('pk')
    serializer_class = TowRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        field_token = request.data.get('mobileToken', None)
        name = request.data.get('Name', None)

        user_id = user

        print('111111')
        try:
            device_token = FCMDevice.objects.create(
                user=user,
                registration_id=field_token,
                name=name
            )
            return Response({'message': 'Token and record saved successfully', 'data': device_token.pk}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle errors gracefully, providing a user-friendly message
            return Response({'error': 'An error occurred while saving the token: ' + str(e)}, status=status.HTTP_200_OK)


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

    # def create(self, request, *args, **kwargs):
    #     request.data._mutable = True
    #     request_data = request.data
    #     password = request.data.get('password')

    #     # Hash the password
    #     hashed_password = make_password(password)

    #     # Update the request data with the hashed password
    #     request.data['password'] = hashed_password
    #     user_info = {}
    #     user_info["user_type"] = "Workshop Owner"
    #     for user_data in request_data:
    #         print(user_data)
    #         user_info[user_data] = request_data.get(user_data, None)

    #     user = UserSerializer(data=user_info)
    #     user.is_valid()
    #     if user.errors:
    #         print(user.errors)
    #     user.is_valid(raise_exception=True)
    #     workshopUser = user.save()
    #     print(workshopUser)
    #     request_data["user_id"] = workshopUser.pk
    #     print('done')
    #     us = User.objects.get(id=workshopUser.pk)
    #     token_serializer = MyTokenObtainPairSerializer()
    #     token = token_serializer.get_token(us)
    #     print(MyTokenObtainPairSerializer)
    #     print(us)
    #     print(token)
    #     # Include the token in the response data
    #     response_data = {
    #         'access': str(token.access_token),
    #         'refresh': str(token),

    #         'user': workshopUser.pk
    #     }
    #     # Return the response
    #     return Response(response_data, status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request_data = request.data
        password = request.data.get('password')

        # Hash the password
        print('pppppp', password)
        hashed_password = make_password(password)
        print("hhhhhhhh", hashed_password)
        # Update the request data with the hashed password
        request.data['password'] = hashed_password
        user_info = {}
        user_info["user_type"] = "Workshop Owner"
        print('rrrrrrrrr', request.data)
        for user_data in request_data:
            print(user_data)
            user_info[user_data] = request_data.get(user_data, None)
        print('uuuuuuuu', user_info)
        user = UserSerializer(data=user_info)
        user.is_valid()
        if user.errors:
            print(user.errors)
        user.is_valid(raise_exception=True)
        workshopUser = user.save()
        print(workshopUser)
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

    def partial_update(self, request, *args, **kwargs):
        serialized = WorkShopOwnerSerializer(
            request.user, data=request.data, partial=True)
        return Response(status=status.HTTP_202_ACCEPTED)


class OriginViewSet (ModelViewSet):
    queryset = Origin.objects.all().order_by('pk')
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


def _send_notification(self, device, title, body):
    conn = http.client.HTTPSConnection("fcm.googleapis.com")
    payload = json.dumps({
        "to": device.registration_id,
        "notification": {
            "title": title,
            "body": body,
            "mutable_content": True,
            "sound": "Tri-tone"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
    }
    conn.request("POST", "/fcm/send", payload, headers)
    res = conn.getresponse()
    data = res.read()


class ThrottledResponse(APIException):
    status_code = 429  # Use HTTP status code for "Too Many Requests"
    default_detail = 'Rate limit exceeded'


class MaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user_id = self.request.user.pk
        owner = CarOwner.objects.get(user_id=user_id)
        try:
            req = Request.objects.filter(userId=owner)
            main = maintenance.objects.filter(requestId__in=req)
            return main
        except CarOwner.DoesNotExist:
            raise NotFound("no request")

    def handle_permission_error(self, request):
        # Check if specific permission error is related to rate limiting
        if isinstance(self.throttled(request=request), ThrottledResponse):
            # Extract remaining time from the exception detail
            detail = self.throttled(request=request).detail
            remaining_seconds = int(detail.split("available in ")[
                                    1].split(" seconds")[0])

            # Return custom response with remaining time information
            return Response({
                "detail": "Rate limit exceeded. Try again in " + str(remaining_seconds) + " seconds."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Raise a generic error if the reason is not related to rate limiting
        raise PermissionDenied(
            "User does not have permission to perform this action.")

    def create(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        try:
            if self.check_permissions(request):

                return self.handle_permission_error(request)
            request.data._mutable = True
            user = self.request.user.pk

            request_data = request.data
            carOwner = CarOwner.objects.get(user_id=user)

            workshop_id = request.data.get('workshopId')
            print("@@!!", workshop_id)
            w = WorkShop.objects.get(id=workshop_id)
            kra = w.workshopOwnerId.user_id
            request.data["userId"] = carOwner.pk
            request.data["transactionStatus"] = 1
            request_info = {}

            try:
                devices = FCMDevice.objects.get(user_id=kra.pk)
                print(devices.registration_id)
                print('ppppppppppppppppppppppppppppppppppppppppp')
                conn = http.client.HTTPSConnection("fcm.googleapis.com")
                payload = json.dumps({
                    "to": devices.registration_id,
                    "notification": {
                        "title": "New Request",
                        "body": "You have new Maintenance Request",
                        "mutable_content": True,
                        "sound": "Tri-tone"
                    },

                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
                }
                conn.request("POST", "/fcm/send", payload, headers)
                res = conn.getresponse()
                data = res.read()
            except FCMDevice.DoesNotExist:
                # Handle case where no device token is found
                print("No device token found for workshop owner")
                return Response({"message": "No device token found for workshop owner"}, status=status.HTTP_400_BAD_REQUEST)

            for data in request_data:
                print(data)
                request_info[data] = request_data.get(data, None)

            serializer = RequestSerializer(data=request_info)
            serializer.is_valid()
            if serializer.errors:
                print(serializer.errors)
            serializer.is_valid(raise_exception=True)
            r1 = serializer.save()

            request_data["requestId"] = r1.pk
            print(request_data)
            print("1234")
            k = maintenanceSerializer(data=request_data,)
            print(k.is_valid())
            k.is_valid()
            if serializer.errors:
                print(serializer.errors)
            k.is_valid(raise_exception=True)
            k.save()

            return Response(request.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle other potential exceptions
            print(f"An error occurred: {e}")
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        user = self.request.user.pk
        request.data._mutable = True
        Owner = CarOwner.objects.get(user_id=user)
        shop = Request.objects.get(id=request_id)
        mai = maintenance.objects.get(requestId=request_id)
        s = int(request.data.get('status', ''))
        print(s)
        if s == 3:
            request.data["transactionStatus"] = 6
        else:
            request.data["transactionStatus"] = 2
        k = WorkShop.objects.get(workshopOwnerId=shop.workshopId.pk)
        w = k.workshopOwnerId.user_id
        devices = FCMDevice.objects.get(user_id=w.pk)
        print('oooooooooooooooooooooooooooooooooooooooooo')
        print(devices.registration_id)
        conn = http.client.HTTPSConnection("fcm.googleapis.com")
        payload = json.dumps({
            "to": devices.registration_id,
            "notification": {
                "title": "New Request",
                "body": "Set Time For Request  ",
                "mutable_content": True,
                "sound": "Tri-tone"
            },

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
        }
        conn.request("POST", "/fcm/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(shop.pk)
        request.data["userId"] = shop.userId.pk
        request.data['requestId'] = request_id
        print('1234')
        request.data["carsId"] = shop.carsId.pk
        print('1235')
        request.data['requestType'] = shop.requestType
        print('12356')
        request.data['workshopId'] = shop.workshopId.pk
        print('12357')
        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        print(shop)
        serializer.is_valid(raise_exception=True)
        print('1235789')
        serializer.update(instance=shop,
                          validated_data=serializer.validated_data)
        k = maintenanceSerializer(
            instance=shop, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=shop, validated_data=k.validated_data)
        print('123578910')

        return Response(serializer.data, status=status.HTTP_200_OK)


class shopMaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        user = self.request.user.pk
        request.data._mutable = True
        shop = Request.objects.get(id=request_id)
        mai = maintenance.objects.get(requestId=request_id)
        Owner = WorkShopOwner.objects.get(user_id=user)
        k = shop.userId.user_id
        devices = FCMDevice.objects.get(user_id=k.pk)
        conn = http.client.HTTPSConnection("fcm.googleapis.com")
        payload = json.dumps({
            "to": devices.registration_id,
            "notification": {
                "title": "New Request",
                "body": "You have Date for Request Accept or Reject  ",
                "mutable_content": True,
                "sound": "Tri-tone"
            },

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
        }
        conn.request("POST", "/fcm/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        s = int(request.data.get('status', ''))
        print(s)
        if s == 3:
            request.data["transactionStatus"] = 6
        else:
            request.data["transactionStatus"] = 3
        request.data["userId"] = shop.userId.pk
        request.data['requestId'] = request_id
        request.data["carsId"] = shop.carsId.pk
        request.data['requestType'] = shop.requestType
        request.data['workshopId'] = shop.workshopId
        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=shop, validated_data=serializer.validated_data)
        k = maintenanceSerializer(
            instance=shop, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=shop, validated_data=k.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def sendNot(request):

#     conn = http.client.HTTPSConnection("fcm.googleapis.com")
#     payload = json.dumps({
#         "to": "cm6WjfQPTRe52hHxO1UGTL:APA91bEr5h46xbTeodEBHEFxxqsXY-nEK7pzgjiTYWYEBaZH4phOxqWXER5kZ-tmSNFZnYXV-tM_5t7NJsyclzc7xsnHy9erhZLR8_ynM360miBvDBkPGDitVsZP3X_pVX4zCRO4Xbra",
#         "notification": {
#             "title": "Check this Mobile (title)",
#             "body": "Rich Notification testing (body)",
#             "mutable_content": True,
#             "sound": "Tri-tone"
#         },

#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
#     }
#     conn.request("POST", "/fcm/send", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     return Response((data.decode("utf-8")))


class shop1MaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        print(request_data)
        user = self.request.user.pk
        request.data._mutable = True
        shop = Request.objects.get(id=request_id)
        mai = maintenance.objects.get(requestId=request_id)
        Owner = WorkShopOwner.objects.get(user_id=user)
        carOwner = shop.userId.user_id
        devices = FCMDevice.objects.get(user_id=carOwner.pk)
        conn = http.client.HTTPSConnection("fcm.googleapis.com")
        payload = json.dumps({
            "to": devices.registration_id,
            "notification": {
                "title": "New Request",
                "body": " Offer Price ",
                "mutable_content": True,
                "sound": "Tri-tone"
            },

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
        }
        conn.request("POST", "/fcm/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        s = int(request.data.get('status', ''))
        print(s)
        if s == 3:
            request.data["transactionStatus"] = 6
        else:
            request.data["transactionStatus"] = 4
        request.data["userId"] = shop.userId.pk
        request.data['requestId'] = request_id
        request.data["carsId"] = shop.carsId.pk
        request.data['requestType'] = shop.requestType
        request.data['workshopId'] = shop.workshopId.workshopOwnerId.pk
        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=shop, validated_data=serializer.validated_data)
        k = maintenanceSerializer(
            instance=mai, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=mai, validated_data=k.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptMaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        user = self.request.user.pk
        request.data._mutable = True
        shop = Request.objects.get(id=request_id)
        mai = maintenance.objects.get(requestId=request_id)
        Owner = CarOwner.objects.get(user_id=user)
        k = shop.workshopId.workshopOwnerId.user_id
        devices = FCMDevice.objects.get(
            user_id=k.pk)
        conn = http.client.HTTPSConnection("fcm.googleapis.com")
        payload = json.dumps({
            "to": devices.registration_id,
            "notification": {
                "title": "New Request",
                "body": "Your Offer has been approved",
                "mutable_content": True,
                "sound": "Tri-tone"
            },

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
        }
        conn.request("POST", "/fcm/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if shop.status == 'CANCELLED':  # Assuming you have a 'status' field
            request.data["transactionStatus"] = 6
        else:
            request.data["transactionStatus"] = 5
        print(shop.pk)
        request.data["userId"] = Owner.pk
        request.data['requestId'] = request_id
        print('1234')
        request.data["carsId"] = shop.carsId.pk
        print('1235')
        request.data['requestType'] = shop.requestType
        print('12356')
        request.data['workshopId'] = shop.workshopId.pk
        print('12357')
        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        print(shop)
        serializer.is_valid(raise_exception=True)
        print('1235789')
        serializer.update(instance=shop,
                          validated_data=serializer.validated_data)
        k = maintenanceSerializer(
            instance=shop, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=shop, validated_data=k.validated_data)
        print('123578910')

        return Response(serializer.data, status=status.HTTP_200_OK)


class shop2MaintenanceViewSet (ModelViewSet):
    queryset = maintenance.objects.all().order_by('pk')
    serializer_class = maintenanceSerializer

    def update(self, request, *args, **kwargs):
        request_id = kwargs.get('pk')
        request_data = request.data
        user = self.request.user.pk
        request.data._mutable = True
        shop = Request.objects.get(id=request_id)
        mai = maintenance.objects.get(requestId=request_id)
        k = shop.userId.user_id.pk
        devices = FCMDevice.objects.get(
            user_id=k)
        conn = http.client.HTTPSConnection("fcm.googleapis.com")
        payload = json.dumps({
            "to": devices.registration_id,
            "notification": {
                "title": "New Request",
                "body": "Your Request has finished",
                "mutable_content": True,
                "sound": "Tri-tone"
            },

        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAMky24Wg:APA91bG5ESVaRrLCG4mIQFN7vFCNLcRLlEcnfBrmDR7uUlPqSXMTlLtaYTnZMKQAWbtAsOpmDmUPvm_6RSO3JKs30-44FKhMBS3dVUdQKgNk-I0BZ9Aw5L67yGPWw8aoyxFywD_viqbO'
        }
        conn.request("POST", "/fcm/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        request.data["transactionStatus"] = 6
        request.data["userId"] = shop.userId.pk
        request.data['requestId'] = request_id
        request.data["carsId"] = shop.carsId.pk
        request.data['requestType'] = shop.requestType
        request.data['workshopId'] = shop.workshopId.pk

        serializer = RequestSerializer(
            instance=shop, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=shop, validated_data=serializer.validated_data)
        k = maintenanceSerializer(
            instance=shop, data=request_data, partial=True)
        k.is_valid(raise_exception=True)
        k.update(instance=shop, validated_data=k.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['available']

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
        car.is_valid()
        if car.errors:
            print(car.errors)
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
        user = self.request.user.pk
        print(user)
        owner = TowCarOwner.objects.get(user_id=user)
        print(owner)
        tow_car = TowCars.objects.get(userId=owner)
        print(tow_car)
        tow_car.available = not tow_car.available
        tow_car.save()
        serializer = self.get_serializer(tow_car)
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
        origins = Origin.objects.all()
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


# class ProductPartViewSet (ModelViewSet):
#     queryset = ProductPartSupplier.objects.filter()
#     serializer_class = ProductPartSupplierSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['partSupplierId']

#     def create(self, request, *args, **kwargs):
#         request.data._mutable = True
#         data = request.data
#         user = self.request.user.pk
#         part_supplier = PartSupplier.objects.get(user_id=user)
#         request.data['partSupplierId'] = part_supplier.pk
#         print("1")
#         print(part_supplier.pk)

#         product_info = {}
#         for product_data in data:
#             product_info[product_data] = data.get(product_data, None)
#             print(product_data)
#         origin_brands = []
#         print(product_info, "@@@@@@@@@@@@")
#         brands = product_info.get('brands', None)
#         brands_list = [int(brand)
#                        for brand in brands.split(',') if brand.isdigit()]
#         print(brands_list)
#         origin_brands = storeBrands.objects.filter(
#             partSupplierId=part_supplier.pk, brands__in=brands_list)

#         print(origin_brands.count(), brands_list.__len__())
#         if origin_brands.count() == brands_list.__len__():
#             for i in origin_brands:
#                 product_info["brands"] = i.brands.pk
#                 print(i.brands.pk)
#                 print(product_info)
#                 print('112344')
#                 product = ProductPartSupplierSerializer(data=product_info)
#                 product.is_valid()
#                 if product.errors:
#                     print(product.errors)

#                 product.is_valid(raise_exception=True)
#                 product.save()

#         return Response(origin_brands.values(), status=status.HTTP_200_OK)

class wPartViewSet(ModelViewSet):
    queryset = ProductPartSupplier.objects.all()  # Use the pre-defined queryset
    serializer_class = WPartSupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['productId']

    # def get_queryset(self):

    #     user_id = self.request.user.pk  # Assuming you need user ID
    #     res = ProductPartSupplier.objects.values('partSupplierId').distinct()

    #     print("22@@", res)

    #     return res
    def list(self, request, *args, **kwargs):
        res = ProductPartSupplier.objects.values_list(
            'partSupplierId').distinct()
        print("@@", res)
        partSup = PartSupplier.objects.filter(id__in=res)
        pp = PartSupplierSerializer(
            partSup, many=True, context={'request': request})
        return Response(pp.data)
        return super().list(request, *args, **kwargs)


class ProductPartViewSet (ModelViewSet):
    queryset = ProductPartSupplier.objects.filter()
    serializer_class = ProductPartSupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partSupplierId', 'productId']
    # permission_classes = [IsAuthenticated, PartSupplierAuth]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_id = self.request.user.pk
            owner = PartSupplier.objects.get(user_id=user_id)
            k = ProductPartSupplier.objects.filter(partSupplierId=owner)
            return k
        else:
            w = ProductPartSupplier.objects.all()
            return w

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        data = request.data
        user = self.request.user.pk
        part_supplier = PartSupplier.objects.get(user_id=user)
        # request.data['partSupplierId'] = part_supplier.pk
        # request.data._mutable = False
        # print(request.data)

        print("1")
        print(part_supplier.pk)
        product = request.data.get('productId')
        model = request.data.get('CarModel')
        product_info = {}
        for i in product.split(','):
            print(i)
            seira = self.get_serializer(
                data={'productId': i, 'CarModel': model, 'partSupplierId': part_supplier.pk})
            seira.is_valid(raise_exception=True)
            seira.save()
        return Response(seira.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.request.user.pk
        print(user)
        owner = PartSupplier.objects.get(user_id=user)
        print(owner)
        tow_car = ProductPartSupplier.objects.get(userId=owner)
        print(tow_car)
        tow_car.status = not tow_car.status
        tow_car.save()
        serializer = self.get_serializer(tow_car)
        return Response(serializer.data)


class CarProductPartViewSet (ModelViewSet):
    queryset = ProductPartSupplier.objects.filter()
    serializer_class = ProductPartSupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partSupplierId', 'productId']
    # permission_classes = [IsAuthenticated, PartSupplierAuth]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         user_id = self.request.user.pk
    #         owner = PartSupplier.objects.get(user_id=user_id)
    #         k = ProductPartSupplier.objects.filter(partSupplierId=owner)
    #         return k
    #     else:
    #         w = ProductPartSupplier.objects.all()
    #         return w


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


class WorkShopUpdateAPIView(APIView):
    def put(self, request, pk, *args, **kwargs):
        workshop_owner = WorkShopOwner.objects.get(user_id=pk)
        print(workshop_owner)
        user = workshop_owner.user_id
        user.email = request.data.get('email', user.email)
        user.fullName = request.data.get('fullName', user.fullName)
        user.set_password(request.data.get('password', user.password))
        user.phoneNumber = request.data.get('phoneNumber', user.phoneNumber)
        user.avatar = request.data.get('avatar', user.avatar)

        user.save()

        workshop = WorkShop.objects.get(workshopOwnerId=workshop_owner)
        workshop.logo = request.data.get('logo', workshop.logo)
        workshop.workshopName = request.data.get(
            'workshopName', workshop.workshopName)
        workshop.contactNumber = request.data.get(
            'contactNumber', workshop.workshopName)
        workshop.save()

        return Response(status=status.HTTP_200_OK)


class PartSupplierUpdateAPIView(APIView):
    def put(self, request, pk, *args, **kwargs):
        #     print('aaaaaaaaaa')
        #     instance = get_object_or_404(User, pk=pk)
        #     print('0aaaaaaaaaa')
        #     serializer = PartSupplierSerializer(instance, data=request.data)
        #     print('1aaaaaaaaaa')
        #     if serializer.is_valid():
        #         serializer.save
        #         return Response(serializer.data)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        part_supplier = PartSupplier.objects.get(user_id=pk)
        user = part_supplier.user_id

        user.avatar = request.data.get('avatar', user.avatar)
        user.email = request.data.get('email', user.email)
        user.fullName = request.data.get('fullName', user.fullName)
        user.set_password(request.data.get('password', user.password))
        user.phoneNumber = request.data.get('phoneNumber', user.phoneNumber)

        user.save()

        part_supplier.logo = request.data.get('logo', part_supplier.logo)
        part_supplier.storeName = request.data.get(
            'storeName', part_supplier.storeName)
        part_supplier.contactNumber = request.data.get(
            'contactNumber', part_supplier.contactNumber)

        part_supplier.save()

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

    existing_origins = Origin.objects.all()

    for origin_name, car_list in cars.items():
        # Get or create the origin object
        origin, created = Origin.objects.get_or_create(name=origin_name)

        # Save brands if origin wasn't created in this loop
        if not created:
            for car_name in car_list:
                brand = Brand(name=car_name, origin=origin)
                brand.save()

    return Response("Brands added successfully.")


class locationsViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TransactionStatusViewSet(ModelViewSet):
    queryset = TransactionStatus.objects.all()
    serializer_class = TransactionStatusSerializer


class RequestTypeViewSet(ModelViewSet):
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer


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
        ori = Origin(name=i)
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
