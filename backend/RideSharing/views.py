from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializer import UserInfoSerializer, loginSerializer, rideInfoSerializer
from .models import UserInfo, rideInfo, vehicleInformation



# @api_view(["GET", "POST"])
# def index(request):
#     routes = [{"first_name": "Ramey", "last_name": "Kuikel", "phoneNumberprin": "9847563258"}]

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
            print(data)
            serializer = UserInfoSerializer(data=data, many=False)
            print(serializer)
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


@api_view(["GET"])
def getOneUserInfo(request, phoneNumber):
    try:
        userinfo = UserInfo.objects.get(phoneNumber=phoneNumber)
        serializer = UserInfoSerializer(userinfo, many=False)
        return Response(
            {
                "status": 200,
                "payload": serializer.data,
                "message": "User information obtained sucessfully",
            }
        )
    except UserInfo.DoesNotExist:
        return Response(
            {
                "status": 404,
                "payload": {},
                "message": "User doesnot exist",
            }
        )


@api_view(['POST'])
def createUser(request):
    data = request.data #-> extract the data part from the post request

    new_user = UserInfo.objects.create(
        first_name=data['firstName'],
        last_name=data['lastName'],
        phoneNumber=data['phone'],
        isRider=data['isRider'],
        current_address=data['currentAddress'],
        dob = data['dateOfBirth'].split('T')[0],
    )

    serializer = UserInfoSerializer(new_user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])  # Put request is to update data
def updateUser(self, request, phoneNumber):  # ---> update the user information
    data = request.data
    try:
        user = UserInfo.objects.get(phoneNumber=phoneNumber)
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
    except UserInfo.DoesNotExist:
        return Response(
            {
                "status": 404,
                "message": "User phone number not found",
                "payload": {},
            }
        )


@api_view(["DELETE"])
def deleteUser(request, phoneNumber):  # --> delete the existing user
    try:
        user = UserInfo.objects.get(phoneNumber=phoneNumber)
        user.delete()
        return Response({"status": 200, "message": "User deleted sucessfully", "data": {}})

    except UserInfo.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User phone number not found",
            "payload": {},

        })




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
        serializer = rideInfoSerializer(user_id=pk)
        print(serializer)
        if serializer.is_valid():
            phoneNumber = serializer.data["phoneNumber"]
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