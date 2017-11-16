from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import BucketlistSerializer, UserSerializer
from .models import Bucketlist
from django.contrib.auth.models import User
from .permissions import IsOwner


class CreateView(generics.ListCreateAPIView):
    """Create bucketlist endpoint."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save post data to db."""
        serializer.save(created_by=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET, PUT, DELETE requests."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
