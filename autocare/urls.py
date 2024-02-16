from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from .views import MyTokenObtainPairView, ToggleTowCarAvailability, CarOwnerUpdateAPIView


routers = DefaultRouter()
routers.register('AddBrand', views.BrandViewSet)
routers.register('AddCheckup', views.CheckupViewSet)
routers.register('AddLocation', views.locViewSet)
routers.register('AddMaintenance', views.MaintenanceViewSet)
routers.register('AddOrigin', views.OriginViewSet)
routers.register('AddRequest', views.RequestViewSet)
routers.register('AddProduct', views.productViewSet)
routers.register('AddTowRequest', views.TowRequestViewSet)
routers.register('AddTowCar', views.TowCarViewSet)
routers.register('AddWorkShop', views.WorkShopViewSet)
routers.register('AddStore', views.StoreViewSet)
routers.register('CreateCarsOwner', views.CarOwnerViewSet)
routers.register('CreateCars', views.CarsViewSet)
routers.register('AddPartStore', views.PartSupplierViewSet)
routers.register('CreateUser', views.UserViewSet)
routers.register('CreateTowCarOwner', views.TowCarOwnerViewSet)
routers.register('CreateWorkShopOwner', views.WorkShopOwnerViewSet)
routers.register('ManageWorkShopImages', views.WorkShopImagesViewSet)
routers.register('ManageOrigin_Brand', views.Origin_BrandViewSet)
routers.register('GetSpecialists', views.SpecialistViewSet)
routers.register('AssignProduct', views.ProductPartViewSet)
routers.register('CarModel', views.CarModelViewSet)
routers.register('TowBrand', views.TowBrandViewSet)
routers.register('TowOrigin', views.TowOriginViewSet)
# routers.register('ToggleTowCarAvailability',
#                  views.ToggleTowCarAvailability, basename="Availability")
routers.register('ImageViewSet', views.ImageViewSet, basename="image")
routers.register('City', views.CityViewSet, basename="city")


routers.urls
urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(routers.urls)),
    path('profile', views.userImagesViewSet.as_view()),
    path('add', views.add),
    path('AddCarModel', views.AddCarModel),
    path('userType', views.userType),
    path('toggleAvailability/<int:pk>/', ToggleTowCarAvailability.as_view()),
    path('car-owner/update/<int:pk>/', CarOwnerUpdateAPIView.as_view(),
         name='car-owner-update'),
    path('AddSpecialist', views.AddSpecialist),
    path('AddOrigin', views.AddOrigin),
    path('AddCity', views.AddCity),
    path('AddProduct', views.AddProduct),
    path('AddTowOrigin', views.AddTowOrigin),
    path('AddTowBrand', views.AddTowBrand),
]
