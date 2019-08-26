
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from rest_framework import status

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

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
        userstatus.location = "unknown"
        userstatus.save()
    token, _= Token.objects.get_or_create(user = user)
    
    return Response({'token': token.key}, status = HTTP_200_OK)
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