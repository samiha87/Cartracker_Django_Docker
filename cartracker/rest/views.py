from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def CreateUser(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                status = HTTP_400_BAD_REQUEST)

    user = authenticate(username = username, password = password)
    if not user:
        user = User.objects.create_user(username=username, password = password)
        #Create userstatus 
        userstatus = UserStatus.objects.create()
        userstatus.username = username
        userstatus.location = "unknown"
        userstatus.save()
    token, _= Token.objects.get_or_create(user = user)
    
    return Response({'token': token.key}, status = HTTP_200_OK)

    @csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def UserLogin(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                status = HTTP_400_BAD_REQUEST)

    user = authenticate(username = username, password = password)
    if not user:
        return Response({'token': 'Failed'}, status = status.HTTP_400_BAD_REQUEST)
    token, _= Token.objects.get_or_create(user = user)
    print("Views::UserLogin() return response: ", token)
    return Response({'token': token.key}, status = HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def UserStatusView(request):
       
    if request.method == 'POST':
        user_status = request.data['status']
        user = request.user.username
        print("UserStatusView, POST ",  user) 
        print("UserStatusView, POST", request.data)
        userstatus = UserStatus.objects.filter(username=user).first()
        #serializer = PostUserStatusSerializer(data = request.data)

        userstatus.status = user_status
        userstatus.save()
        return Response("Ok", status = status.HTTP_200_OK)

        @csrf_exempt

@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def UpdateCoordinates(request):
    print(request.user.username + " UpdateCoordinates")
    if request.method == 'POST':
        userstatus = UserStatus.objects.filter(username = request.user.username).first()
        #Validate
        print("UpdateCoordinates ", request.user.username)
        print("UpdateCoordinates ", request.data)
        if request.data.get('longitude') and request.data.get('latitude') and request.data.get('altitude'):
           # print("valid")
            coordinates = GPSCoordinates.objects.create(userstatus_gps = userstatus)
            coordinates.longitude = request.data.get('longitude')
            coordinates.latitude = request.data.get('latitude')
            coordinates.altitude = request.data.get('altitude')
            coordinates.save()
            userstatus.location = getLocation(coordinates)
            userstatus.save()
            return Response(userstatus.location, status = status.HTTP_201_CREATED)
        else:
            return Response("Check your json", status = status.HTTP_400_BAD_REQUEST)

