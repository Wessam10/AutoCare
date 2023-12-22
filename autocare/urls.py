from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

routers = DefaultRouter()
routers.register('RegisterWorkShop', views.WorkShopViewSet)
routers.register('ManageRequest', views.RequestViewSet)
routers.register('ManageBrand', views.BrandViewSet)
routers.register('CreateCarOwner', views.CarOwnerViewSet)
routers.register('ManageCars', views.CarsViewSet)
routers.register('ManagePartSupplier', views.PartSupplierViewSet)
routers.register('ManageProduct', views.productViewSet)
routers.register('ManageTowCarOwner', views.TowCarOwnerViewSet)
routers.register('ManageTowRequest', views.TowRequestViewSet)
routers.register('ManageUser', views.UserViewSet)
routers.register('ManageWorkShopOwner', views.WorkShopOwnerViewSet)
routers.register('ManageOrigin', views.OriginViewSet)
routers.register('manageCheckup', views.CheckupViewSet)
routers.register('manageLocation', views.locViewSet)
routers.register('manageMaintenance', views.MaintenanceViewSet)
routers.register('manageWorkShopImages', views.WorkShopImagesViewSet)


routers.urls
urlpatterns = [
    path('', include(routers.urls)),
    path('profile', views.userImagesViewSet.as_view()),
    # path('add', views.add)
]
