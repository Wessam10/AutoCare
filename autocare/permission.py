from rest_framework.permissions import BasePermission, IsAuthenticated
from AutoC.settings import SECRET_KEY
from autocare.models import CarOwner, WorkShopOwner, PartSupplier, TowCarOwner
import jwt


# def decode_token(token: str) -> User:
# username = jwt.decode(
#     token, SECRET_KEY, algorithms=['HS256'])
# user = User.objects.filter(id=username["id"])
# if user.exists():
#     return {"user": user.first()}


class CarOwnerAuth(BasePermission):
    def has_permission(self, request, view):
        print(request.user.pk)
        user = request.user.pk
        if CarOwner.objects.filter(user_id=user).exists():
            print("CarOwner.objects.get(user_id=user)")
            return True
        print("aaaaaaaaa")
        return False


class workshopOwnerAuth(BasePermission):
    def has_permission(self, request, view):
        print(request.user.pk)
        user = request.user.pk
        if WorkShopOwner.objects.filter(user_id=user).exists():
            print("aaaaaaaaa")
            return True
        return False
