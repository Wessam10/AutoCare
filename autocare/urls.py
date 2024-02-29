from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from .views import MyTokenObtainPairView, ToggleTowCarAvailability, TowRequestViewSet, CarOwnerUpdateAPIView, PartSupplierUpdateAPIView, WorkShopUpdateAPIView, RequestViewSet


routers = DefaultRouter()
routers.register('AddBrand', views.BrandViewSet)
routers.register('AddCheckup', views.CheckupViewSet)
routers.register('AddLocation', views.locViewSet)
routers.register('CarMaintenance', views.MaintenanceViewSet)
routers.register('shopMaintenance', views.shopMaintenanceViewSet)
routers.register('evaluateMaintenance', views.shop1MaintenanceViewSet)
routers.register('AcceptPriceDealMaintenance',
                 views.AcceptMaintenanceViewSet)
routers.register('FinishedMaintenance', views.shop2MaintenanceViewSet)
routers.register('AddOrigin', views.OriginViewSet)
routers.register('AddRequest', views.RequestViewSet)
routers.register('CarOwnerRequest', views.CarOwnerRequestViewSet)
routers.register('AddProduct', views.productViewSet)
routers.register('AddTowRequest', views.TowRequestViewSet)
routers.register('AddTowCar', views.TowCarViewSet)
routers.register('AddWorkShop', views.WorkShopViewSet)
routers.register('AddStore', views.StoreViewSet)
routers.register('CreateCarsOwner', views.CarOwnerViewSet)
routers.register('CreateCars', views.CarsViewSet)
routers.register('CurrentCars', views.CurrentCarsViewSet)
routers.register('AddPartStore', views.PartSupplierViewSet)
routers.register('CreateUser', views.UserViewSet)
routers.register('CreateTowCarOwner', views.TowCarOwnerViewSet)
routers.register('CreateWorkShopOwner', views.WorkShopOwnerViewSet)
routers.register('ManageWorkShopImages', views.WorkShopImagesViewSet)
routers.register('ManageOrigin_Brand', views.Origin_BrandViewSet)
routers.register('GetSpecialists', views.SpecialistViewSet)
routers.register('AssignProduct', views.ProductPartViewSet)
routers.register('CarProductPart', views.CarProductPartViewSet)
routers.register('wPart', views.wPartViewSet)
routers.register('CarModel', views.CarModelViewSet)
routers.register('TowBrand', views.TowBrandViewSet)
routers.register('TowOrigin', views.TowOriginViewSet)
routers.register('tokenDevice', views.tokenDeviceViewSet)
routers.register('Status', views.StatusViewSet)
routers.register('TransactionStatus', views.TransactionStatusViewSet)
routers.register('RequestType', views.RequestTypeViewSet)
routers.register('brandStore', views.brandStoreViewSet)
routers.register('ExcludeRequest', views.ExcludeRequestViewSet)
# routers.register('ToggleTowCarAvailability',
#                  views.ToggleTowCarAvailability, basename="Availability")
routers.register('ImageViewSet', views.ImageViewSet, basename="image")
routers.register('City', views.CityViewSet, basename="city")


routers.urls
urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get-distance-for-all-cars', TowRequestViewSet.as_view(
        {'get': 'get_distance_for_all_cars'}), name='get-distance-for-all-cars'),
    path('', include(routers.urls)),
    path('profile', views.userImagesViewSet.as_view()),
    path('add', views.add),
    #     path('sendNot', views.sendNot),
    path('AddCarModel', views.AddCarModel),
    path('userType', views.userType),
    path('toggleAvailability', ToggleTowCarAvailability.as_view()),
    path('car-owner/update/<int:pk>/', CarOwnerUpdateAPIView.as_view(),
         name='car-owner-update'),
    path('workshop/update/<int:pk>/',
         WorkShopUpdateAPIView.as_view(), name='workshop-update'),
    path('part-supplier/update/<int:pk>/', PartSupplierUpdateAPIView.as_view(),
         name='part-supplier-update'),
    #     path('requests/<int:pk>/', RequestViewSet.as_view(
    #         {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='request-detail'),
    path('AddSpecialist', views.AddSpecialist),
    path('AddOrigin', views.AddOrigin),
    path('AddCity', views.AddCity),
    path('AddProduct', views.AddProduct),
    path('AddTowOrigin', views.AddTowOrigin),
    path('     ', views.AddTowBrand),
]
