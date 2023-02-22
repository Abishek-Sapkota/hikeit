from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserInfoSerializer, loginSerializer, rideInfoSerializer
from .models import UserInfo, rideInfo, vehicleInformation
from .authenticate import authenticateUser


# @api_view(["GET", "POST"])
# def index(request):
#     routes = [{"first_name": "Ramey", "last_name": "Kuikel", "ph_number": "9847563258"}]

#     return Response(routes)



class userInformation(APIView):  # --> classbased api view
    def get(self, request):  # --> this just list all the users
        userinfo = UserInfo.objects.all()
        serializer = UserInfoSerializer(
            userinfo, many=True
        )  # -> serializes the userinfo for frontend
        print(serializer.data)
        return Response(
            {
                "status": 200,
                "payload": serializer.data,
                "message": "Everthing looks good",
            }
        )

    def post(self, request):  # --> create new user
        try:
            data = request.data  # -> extract the data part from the post request
            serializer = UserInfoSerializer(data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": 200,
                        "payload": serializer.data,
                        "message": "User created sucessfully",
                    }
                )
            return Response({"status": 400, "message": "Something went wrong"})
        except Exception as e:
            print(e)



# @api_view(['GET'])
# def getUserInfo(request):
# 	userinfo = UserInfo.objects.all()
# 	serializer = UserInfoSerializer(userinfo, many=True) #-> serializes the userinfo for frontend
# 	return Response(serializer.data)



@api_view(["GET"])
def getOneUserInfo(request, ph_number):
    try:
        userinfo = UserInfo.objects.get(ph_number=ph_number)
        print(userinfo)
        serializer = UserInfoSerializer(userinfo, many=False)
        print(serializer.data)
        return Response(
            {
                "status": 200,
                "payload": serializer.data,
                "message": "User information obtained sucessfully",
            }
        )
    except:
        return Response(
            {
                "status": 400,
                "payload": {},
                "message": "User doesnot exist",
            }
        )



# @api_view(['POST'])
# def createUser(request):
# data = request.data #-> extract the data part from the post request

# new_user = UserInfo.objects.create(
# 	first_name=data['first_name'],
# 	last_name=data['last_name'],
# 	ph_number=data['ph_number']
# )
# serializer = UserInfoSerializer(new_user, many=False)
# return Response(serializer.data)


@api_view(["PUT"])  # Put request is to update data
def updateUser(self, request, ph_number):  # ---> update the user information
    data = request.data
    try:
        user = UserInfo.objects.get(ph_number=ph_number)
        for key, value in data.items():
            setattr(user, key, value)
            user.save()
        # UserInfo.objects.filter(id=pk).update(**data) --> Direct method bypass object.save()
        serializer = UserInfoSerializer(user, many=False)
        return Response(
            {
                "status": 201,
                "payload": serializer.data,
                "message": "User info updated sucessfully",
                "payload": {},
            }
        )
    except:
        return Response(
            {
                "status": 403,
                "error": "User id not found",
                "message": "task unsuccessful",
                "payload": {},
            }
        )



@api_view(["DELETE"])
def deleteUser(request, ph_number):  # --> delete the existing user
    user = UserInfo.objects.get(ph_number=ph_number)
    user.delete()
    return Response({"status": 200, "message": "User deleted sucessfully", "data": {}})


class authenticateUser(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = loginSerializer(data=data)

            if serializer.is_valid():
                ph_number = serializer.data["ph_number"]

                try:
                    user = UserInfo.objects.get(ph_number=ph_number)
                    serializer = UserInfoSerializer(user, many=False)
                # user = authenticate(username=ph_number)

                except:
                    return Response(
                        {"status": 400, "message": "Invalid phone number", "payload": {}}
                    )
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "status": 200,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "payload": serializer.data,
                    }
                )

            return Response({"status": 400, "message": "Something went wrong"})

        except Exception as e:
            print(e)


class storeRideInfo(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = rideInfoSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": 200,
                        "payload": serializer.data,
                        "message": "Location saved",
                    }
                )

        except:
            return Response(
                {
                    "status": 400,
                    "error": serializer.errors,
                    "message": "Something went wrong",
                }
            )


@api_view(["GET"])
def getLoci(request, pk):
    try:
        data = request.data
        queryset = rideInfo.objects.filter(user_id=pk)
        serializer = rideInfoSerializer(id=pk)
        print(serializer)
        if serializer.is_valid():
            ph_number = serializer.data["ph_number"]
            return Response(
                {
                    "status": 200,
                    "payload": serializer.data,
                    "message": "Location history",
                }
            )
        return Response(
            {
                "status": 400,
                "message": "something went wrong",
            }
        )

    except:
        return Response(
            {
                "status": 404,
                "message": "something went wrong",
            }
        )

# class shareRide(APIView):
#     class get(self, request):
#         try:
#             data = request.data
