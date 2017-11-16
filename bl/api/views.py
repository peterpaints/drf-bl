from django.shortcuts import render
from rest_framework import generics
from .serializers import BucketlistSerializer
from .models import Bucketlist


class CreateView(generics.ListCreateAPIView):
    """Create bucketlist endpoint."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        """Save post data to db."""
        serializer.save(created_by=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET, PUT, DELETE requests."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
