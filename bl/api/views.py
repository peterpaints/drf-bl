from rest_framework import generics, permissions
from .serializers import BucketlistSerializer, ItemSerializer, UserSerializer
from .models import Bucketlist, Item
from django.contrib.auth.models import User
from .permissions import IsOwner


class BucketlistView(generics.ListCreateAPIView):
    """Create bucketlist endpoint."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save post data to db."""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """Implement searching with parameter 'q'."""
        queryset = Bucketlist.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
        return queryset


class BucketlistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET, PUT, DELETE requests."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ItemView(generics.ListCreateAPIView):
    """Create item endpoint."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save post data to db."""
        serializer.save()


class ItemDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET, PUT, DELETE requests."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = 'id'
    lookup_url_kwarg = 'pk2'


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    """View to register a user."""
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
