
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import GPSCoordinates, UserStatus

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

# Create new user if user doesn't exist
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((AllowAny,))
def createUser(username, password):
    user = authenticate(username = username, password = password)
    if not user:
        user = User.objects.create_user(username=username, password = password)
        #Create userstatus 
        userstatus = UserStatus.objects.create()
        userstatus.username = username
        userstatus.save()
        token, _= Token.objects.get_or_create(user = user)
        return Response({'token': token.key}, status = HTTP_200_OK)
    if user:
        # If user exist check that userstatus model exist
        userstatus = UserStatus.objects.filter(username = user).first()
        # If userstatus model doesn't exist create one
        if not userstatus:
            userstatus = UserStatus.objects.create()
            userstatus.username = username
            userstatus.save()

    return Response("User exist", status = status.HTTP_400_BAD_REQUEST)
    
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((AllowAny,))
def login(username, password):
    user = authenticate(username = username, password = password)
    if not user:
        return Response({'token': 'Failed'}, status = status.HTTP_400_BAD_REQUEST)
    token, _= Token.objects.get_or_create(user = user)
    return Response({'token': token.key}, status = HTTP_200_OK)

def validateUser(username, password):
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                status = HTTP_400_BAD_REQUEST)
    return True

def getCoordinates(userstatus):
    # Check if usestatus exist
    if userstatus:
        coordinates = GPSCoordinates.objects.filter(userstatus_gps = userstatus).first()
        # check that coordinates exist
        if coordinates:
            # Create response
            content = {'latitude':coordinates.latitude, 'longitude': coordinates.longitude, 'altitude': coordinates.altitude}
            return Response(content, status = status.HTTP_200_OK)
    return Response("Something went wrong, couldn't find coordinates", status = status.HTTP_400_BAD_REQUEST)
