from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    """
    CRUD mechanism for :model:`users.User` using DRF
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        """
        Detail view of user
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


