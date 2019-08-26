from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from .models import UserStatus, GPSCoordinates
from .viewHelper import createUser, login, validateUser

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def CreateUserView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    output = validateUser(username, password)
    if output is True:
        createUser(username, password)
        return createUser(username, password)
    return output

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def LoginView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    output = validateUser(username, password)
    if output is True :
        return login(username, password)
    return output

@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def UserStatusView(request):
       
    if request.method == 'POST':
        user_status = request.data['status']
        user = request.user.username
        userstatus = UserStatus.objects.filter(username=user).first()
        userstatus.status = user_status
        userstatus.save()
        return Response("Ok", status = status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def CoordinatesView(request):
    if request.method == 'POST':
        userstatus = UserStatus.objects.filter(username = request.user.username).first()
        if request.data.get('longitude') and request.data.get('latitude') and request.data.get('altitude'):
            coordinates = GPSCoordinates.objects.create(userstatus_gps = userstatus)
            coordinates.longitude = request.data.get('longitude')
            coordinates.latitude = request.data.get('latitude')
            coordinates.altitude = request.data.get('altitude')
            coordinates.save()
            return Response(userstatus.location, status = status.HTTP_201_CREATED)
        else:
            return Response("Check your json", status = status.HTTP_400_BAD_REQUEST)

