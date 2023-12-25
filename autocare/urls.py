from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from .views import MyTokenObtainPairView


routers = DefaultRouter()
routers.register('AddOrigin', views.OriginViewSet)
routers.register('AddCheckup', views.CheckupViewSet)
routers.register('AddLocation', views.locViewSet)
routers.register('AddMaintenance', views.MaintenanceViewSet)
routers.register('AddRequest', views.RequestViewSet)
routers.register('AddProduct', views.productViewSet)
routers.register('AddBrand', views.BrandViewSet)
routers.register('AddTowRequest', views.TowRequestViewSet)
routers.register('AddWorkShop', views.WorkShopViewSet)
routers.register('CreateCarsOwner', views.CarOwnerViewSet)
routers.register('CreateCars', views.CarsViewSet)
routers.register('CreatePartSupplier', views.PartSupplierViewSet)
routers.register('CreateUser', views.UserViewSet)
routers.register('CreateTowCarOwner', views.TowCarOwnerViewSet)
routers.register('CreateWorkShopOwner', views.WorkShopOwnerViewSet)
routers.register('ManageWorkShopImages', views.WorkShopImagesViewSet)


routers.urls
urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(routers.urls)),
    path('profile', views.userImagesViewSet.as_view()),
    # path('add', views.add)
    path('userType', views.userType),
    path('GetSpecialists', views.GetSpecialist),
    # path('AddSpecialist', views.AddSpecialist)
]
