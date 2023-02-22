from .models import UserInfo
from .serializer import UserInfoSerializer


def authenticateUser(ph_number):
    try:
        print("test5")
        user = UserInfo.objects.get(ph_number= ph_number)
        print("test6")
        return user

    except:
        return None




