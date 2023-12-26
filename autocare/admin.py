from django.contrib import admin
from . models import User, origin, TowCarOwner, Brand, WorkShop, WorkShopOwner, location, CarOwner, Cars, Specialist, workshopBrands, location, City

admin.site.register(User)
admin.site.register(origin)
admin.site.register(Brand)
admin.site.register(WorkShopOwner)
admin.site.register(WorkShop)
admin.site.register(location)
admin.site.register(CarOwner)
admin.site.register(Cars)
admin.site.register(workshopBrands)
admin.site.register(Specialist)
admin.site.register(TowCarOwner)
admin.site.register(City)
# Register your models here.
